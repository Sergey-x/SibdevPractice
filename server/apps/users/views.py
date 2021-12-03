from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from .serializers import BaseCustomUserSerializer, CreateCustomUserSerializer


class CustomUserCreateView(CreateAPIView):
    """
    Create new instance of CustomUser.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateCustomUserSerializer


class CustomUserInfoView(RetrieveAPIView):
    """
    Get base user-info: `username`, `id`.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BaseCustomUserSerializer

    def get_object(self):
        return self.request.user
