from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, UserSerializer


User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user, context={'request': request}).data
        return Response({
        'user': user_data,
        'token': token.key
},      status=status.HTTP_201_CREATED)


class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = (permissions.AllowAny,)


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
        context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user, context={'request': request}).data
        return Response({'token': token.key, 'user': user_data})


class ProfileAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)


    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True, context=       {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
 
