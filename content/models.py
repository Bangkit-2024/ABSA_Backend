import uuid
from django.db import models
from django.contrib.auth.models import User

# This Base model is an abscract class only
class BaseModels(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Company(BaseModels):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return self.name

class Review(BaseModels):
    review_text = models.CharField(max_length=500)
    review_date = models.DateTimeField(null=True,blank=True)
    rating = models.PositiveIntegerField(null=True,blank=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    is_predict_fail = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.review_text

class ReviewAspectSentimentMeta(BaseModels):
    aspect = models.CharField(max_length=50,choices=(
        ["rasa","rasa"],["tempat","tempat"],["harga","harga"],["pelayanan","pelayanan"]
    ),null=True)
    sentiment = models.IntegerField(choices=(
        (-1,"Negatif"),
        (0,"Netral"),
        (1,"Positif")
    ))

    def __str__(self) -> str:
        return f"{self.review} ({self.aspect}) {self.sentiment}"

    class Meta:
        abstract = True

class PredictedReviewAspectSentiment(ReviewAspectSentimentMeta):
    span = models.CharField(max_length=30,null=True)
    review = models.ForeignKey(Review,on_delete=models.CASCADE,related_name="review_aspect")

class RealReviewAspectSentiment(ReviewAspectSentimentMeta):
    review = models.ForeignKey(Review,on_delete=models.CASCADE,related_name="real_review_aspect")
    verified_by = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)