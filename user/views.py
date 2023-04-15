from rest_framework import generics

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create user API"""
    serializer_class = UserSerializer
