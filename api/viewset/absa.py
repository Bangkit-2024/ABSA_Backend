# Depedency
from rest_framework import viewsets, permissions

# Custom Permission
from api.permissions import IsNotEditable

# Models
from content.models import Review

# Serializer
from api.serializers.absa import ReviewSerializer

class ReviewViewset(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsNotEditable]
    
    def get_queryset(self):
        
        return Review.objects.filter(company__user_to_company=self.request.user).all()
    

