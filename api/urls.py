from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

# Ini untuk auth viewset
from api.viewset.auth import RegisterView, ProfileViewSet
from api.viewset.services import TranslateServicesView

# Ini untuk dataviewset
from api.viewset.absa import ReviewViewset

# Ini Router yang diregister
router = routers.DefaultRouter()
router.register(r'review',ReviewViewset,basename='review')

urlpatterns = [
    path('',include(router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('auth/profile/', ProfileViewSet.as_view({
        'get': 'retrieve',
        'patch':'patch',
        'delete':'delete_google_link'
    }), name='user_profile'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('service/translate/',TranslateServicesView.as_view(),name='service-translate')
]