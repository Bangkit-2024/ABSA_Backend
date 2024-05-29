from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import os

class UploadReviewsSerializer(serializers.Serializer):
    review_file = serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv','xlsx'])])