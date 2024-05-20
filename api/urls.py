from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

# Ini untuk auth viewset
from api.viewset.auth import RegisterView, ProfileViewSet

# Ini untuk dataviewset


router = routers.DefaultRouter()

urlpatterns = [
    path('',include(router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('auth/profile/', ProfileViewSet.as_view({
        'get': 'retrieve',
        'patch':'patch',
        'delete':'delete_google_link'
    }), name='user_profile'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
]