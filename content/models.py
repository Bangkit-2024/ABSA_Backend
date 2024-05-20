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
    description = models.CharField(max_length=500)
    user_to_company = models.ManyToManyField(User)

class Review(BaseModels):
    review_text = models.CharField(max_length=500)
    review_date = models.DateTimeField(null=True,blank=True)
    rating = models.PositiveIntegerField()
    company = models.ForeignKey(Company,on_delete=models.CASCADE)

class Aspect(models.Model):
    name = models.CharField(max_length=20)
 
class ReviewAspectSentiment(BaseModels):
    review = models.ForeignKey(Review,on_delete=models.CASCADE)
    aspect = models.ForeignKey(Aspect,on_delete=models.SET_NULL,null=True)
    sentiment = models.IntegerField(choices=(
        (-1,"Negatif"),
        (0,"Netral"),
        (1,"Positif")
    ))