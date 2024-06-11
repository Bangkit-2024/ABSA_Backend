# Disini untuk depedency
from rest_framework import generics, mixins,viewsets, response, status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
import os


# Disini untuk serializer
from api.serializers.auth import UserSerializer, LoginSerializer, ProfileSerializer

# Disini untuk models
from authentication.models import Profile

# Disini untuk services

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class ProfileViewSet(mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            user = self.request.user
            return Profile.objects.filter(user=user)
        except:
            return []

    def retrieve(self, request, *args, **kwargs):
        instance = Profile.objects.filter(user=self.request.user).first()
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = Profile.objects.filter(user=self.request.user).first()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return response.Response(ProfileSerializer(
            Profile.objects.filter(user=self.request.user).first()).data,
                                 status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False)
    def delete_photo(self, request, *args, **kwargs):
        instance = Profile.objects.filter(user=self.request.user).first()
        if instance.photo:
            if os.path.isfile(instance.photo.path):
                os.remove(instance.photo.path)
                instance.photo = None
                instance.save()
                return response.Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)
        return response.Response({"message": "Tidak Ada File Profile"}, status=status.HTTP_400_BAD_REQUEST)
