from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from .auth import is_token_expired
from .models import User
from .serializers import UserSerializer, AuthTokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    
class CustomAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        
        # Extend token expiration
        if not created:
            token.created = timezone.now()
            token.save()

        is_expired = is_token_expired(token)
        if is_expired:
            token.delete()
            token = Token.objects.create(user=token.user)
        return Response({"token": token.key})
