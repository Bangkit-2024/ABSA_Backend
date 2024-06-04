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
from services.absa.setfit_predict import predict_data

class ReviewViewset(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsNotEditable]
    
    def get_queryset(self):
        
        return Review.objects.filter(company__user_to_company=self.request.user).all()
    

    @action(methods=['POST'],detail=False)
    def upload(self,request):

        file = UploadReviewsSerializer(data=request.data)
        if file.is_valid():
            file_obj = request.data['review_file']
            # ...
            # do some stuff with uploaded file
            # ...
            print(pd.read_csv(file_obj))
            
            return response.Response({"message":"Data Berhasil Di Upload"},status=status.HTTP_201_CREATED)
        
        return response.Response({"message":"Terjadi Kesalahan","error":file.error_messages},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(methods=["POST"],detail=False)
    def predict(self,request):

        text_predict = request.data['text']

        return response.Response(predict_data(text_predict),status=status.HTTP_201_CREATED)

