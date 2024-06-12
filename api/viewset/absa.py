# Depedency

from rest_framework import viewsets, permissions, response, status
from rest_framework.decorators import action
from django.db import transaction
import pandas as pd

# Custom Permission
from api.permissions import IsNotEditable

# Models
from content.models import Review, Company, PredictedReviewAspectSentiment, RealReviewAspectSentiment

# Serializer
from api.serializers.absa import ReviewSerializer
from api.serializers.uploads import UploadReviewsSerializer

# Other
from services.services import predict_services, sentiment_output_converter
from services.upload.handle_upload import (
    handle_bulk_aspect_based_review, is_content_valid, 
    handle_bulk_review_only, is_header_include_absa)

class ReviewViewset(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsNotEditable]
    
    def get_queryset(self):
        try:
            return Review.objects.filter(company=self.request.user.profile.company).all()
        except:
            return []
    

    @action(methods=['POST'],detail=False)
    def upload(self,request):

        file = UploadReviewsSerializer(data=request.data)
        error_message = ""
        if file.is_valid():
            file_obj = request.data['review_file']
            content_type = file_obj.content_type
            try:
                if(content_type=="text/csv"):
                    df = pd.read_csv(file_obj)

                elif(content_type=="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
                    df = pd.read_excel(file_obj)

                else:
                    raise ValueError("Format file is not correct")    

                df['company'] = request.user.profile.company.id
                # Check Content (is_ignored=False, more strict about data, it will only give true if data is not empty)
                if not is_content_valid(df,request.data.get('is_ignored',False)):
                    raise ValueError("Content is not correct please read instruction")
                
                if is_header_include_absa(df):
                    handle_bulk_aspect_based_review(request,df)

                else:
                    
                    handle_bulk_review_only(request,df)

                
                return response.Response({"message":"Data Berhasil Di Upload"},status=status.HTTP_201_CREATED)

            except Exception as error:
                return response.Response({"message":f"Terjadi Kesalahan {error}","error":error_message},status=status.HTTP_400_BAD_REQUEST)

        
        return response.Response({"message":"Terjadi Kesalahan","error":error_message},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(methods=["POST"],detail=False)
    def predict(self,request):

        text_predict = request.data.get('text')
        predict = predict_services(text_predict)

        if not text_predict:
            return response.Response({"message":f"Text column should be exist"},status=status.HTTP_400_BAD_REQUEST)

        try:
            predict = predict_services(text_predict)
            return response.Response(predict,status=status.HTTP_201_CREATED)
        
        except Exception as error:
            return response.Response({"message":f"There is Some Error {error}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=["POST"],detail=False)
    def bulk_predict(self,request):

        SUCCESS = 0
        FAILED_COUNT = 0
        errors = []

        user_company = self.request.user.profile.company
        user_review = PredictedReviewAspectSentiment.objects.filter(review__company=user_company).all()
        review_target : list[Review] = Review.objects.filter(company=user_company).filter(is_predict_fail=False).all()

        with transaction.atomic():
            for review_item in review_target:
                try:
                    predict = predict_services(review_item.review_text)
                    span = predict['span']
                    absa = predict['absa']

                    for s,a in zip(span,absa):
                        pred = PredictedReviewAspectSentiment(
                            span=s['span'],
                            aspect=a['aspect'],
                            sentiment=sentiment_output_converter(a['sentiment']),
                            review=review_item
                        )
                        pred.save()

                    SUCCESS+=1
                except Exception as error:
                    # review_item.is_predict_fail = True
                    # review_item.save()
                    errors.append(str(error))
                    FAILED_COUNT+=1

            http_status=status.HTTP_201_CREATED
            if FAILED_COUNT==0:
                message = "Successfuly"
            elif SUCCESS == 0:
                message = "Failed"
                http_status = status.HTTP_400_BAD_REQUEST
            else:
                message = "Partially Successful"
                
            return response.Response({
                "message":f"Data {message} predicted",
                "success_count":SUCCESS,
                "failed_count":FAILED_COUNT,
                "errors":errors
                },status=http_status)

    @action(methods=["POST"],detail=True)
    def verify_review(self, request, pk=None):
        review = Review.objects.filter(id=pk).first()

        aspect_list = request.data.get("aspects")
        sentiment_list = request.data.get("sentiments")

        if (not aspect_list and not sentiment_list ):

            return response.Response({"message":"Input is not correct"},status=status.HTTP_400_BAD_REQUEST)
        
        aspect_list = aspect_list.split(",")
        sentiment_list = sentiment_list.split(",")

        if (len(aspect_list)!=len(sentiment_list)):
            return response.Response({"message":"Input is not correct","error":"Sentiment List Should equal Aspect List"},status=status.HTTP_400_BAD_REQUEST)

        
        with transaction.atomic():
            RealReviewAspectSentiment.objects.filter(review=review).delete()
            try:
                for aspect,sentiment in zip(aspect_list,sentiment_list):

                    if(str(sentiment) not in ['0','-1','1']):
                        return response.Response({"message":"Input is not correct","error":"Sentiment should be number from (-1,0,1) "},status=status.HTTP_400_BAD_REQUEST)
 

                    r= RealReviewAspectSentiment(
                        review = review,
                        aspect=aspect,
                        sentiment=sentiment
                    )

                    r.save()

                return response.Response({"message":"Success"},status=status.HTTP_200_OK)
            except Exception as error:
                print(error)
                return response.Response({"message":"Input is not correct"},status=status.HTTP_400_BAD_REQUEST)
