import factory
from django.contrib.auth.models import User
import factory.fuzzy
from random import choice
from .models import Company, Review, ReviewAspectSentiment

class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company
    
    name = factory.Faker("company")
    location = factory.Faker("address",locale="id_ID")
    description = factory.Faker("paragraph",nb_sentences=15)

    @factory.post_generation
    def user_to_company(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for user in extracted:
                self.user_to_company.add(user)
 

class ReviewFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Review

    review_text = factory.Faker("sentence",nb_words=10)

    @factory.lazy_attribute
    def company(self):
        company = Company.objects.all()
        if Company.objects.exists():
            return choice(company)
        else:
            return CompanyFactory.create()

class ReviewAspectSentimentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ReviewAspectSentiment
    
    sentiment = factory.fuzzy.FuzzyInteger(-1,1)
    aspect = factory.fuzzy.FuzzyChoice(["rasa","tempat","harga","pelayanan"])
        
    @factory.lazy_attribute
    def review(self):
        aspects = Review.objects.all()
        if Review.objects.exists():
            return choice(aspects)