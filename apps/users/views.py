from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import AllowAny

from apps.users.serializers import UserRegisterSerializer, ForgotPasswordSerializer, PasswordResetSerializer


class UserRegisterView(generics.CreateAPIView):
    permission_class = (AllowAny, )
    serializer_class = UserRegisterSerializer


class ForgotPasswordView(generics.CreateAPIView):
    permission_class = (AllowAny, )
    serializer_class = ForgotPasswordSerializer


class PasswordResetView(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny, )
