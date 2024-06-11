from django.contrib import admin
from .models import  Company, Review, ReviewAspectSentiment

# Register your models here.
admin.site.register(Review)
admin.site.register(ReviewAspectSentiment)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    filter_horizontal = ("user_to_company", )