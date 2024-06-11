# Depedency

from rest_framework import viewsets, permissions, response, status
from rest_framework.decorators import action
import pandas as pd

# Custom Permission
from api.permissions import IsNotEditable

# Models
from content.models import Review

# Serializer
from api.serializers.absa import ReviewSerializer
from api.serializers.uploads import UploadReviewsSerializer

# Other
from services.services import predict_services
from services.upload.handle_upload import (
    handle_bulk_aspect_based_review, is_content_valid, 
    handle_bulk_review_only, is_header_include_absa)

class ReviewViewset(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsNotEditable]
    
    def get_queryset(self):
        
        return Review.objects.filter(company__user_to_company=self.request.user).all()
    

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
                # Check Content
                if not is_content_valid(df,request.data['is_ignored']):
                    raise ValueError("Content is not correct please read instruction")
                
                if is_header_include_absa(df):
                    handle_bulk_aspect_based_review(df)
                else:
                    handle_bulk_review_only(df)

                
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



