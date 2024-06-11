from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from content.models import Review, ReviewAspectSentiment

class ReviewAspectBasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewAspectSentiment
        fields = ("id","aspect","sentiment")
    
    def to_representation(self, instance : ReviewAspectSentiment):
        rep =  super().to_representation(instance)
        return rep

class ReviewSerializer(serializers.ModelSerializer):
    review_aspect = ReviewAspectBasedSerializer(many=True, read_only=True)
    class Meta:
        model = Review
        fields = ("id","review_text","company","company_id","review_aspect")
    
    def to_representation(self, instance : Review):
        rep =  super().to_representation(instance)
        rep["company"] = instance.company.name
        rep["company_id"] = instance.company.id
        return rep
    
    