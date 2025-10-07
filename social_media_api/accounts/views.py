from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response, get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, UserSerializer, UserPublicSerializer


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
    
class FollowUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, pk=user_id)
        if request.user == target:
            return Response({"detail": "Cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.follow(target)
        return Response({"detail": f"You are now following {target.username}."}, status=status.HTTP_200_OK)

class UnfollowUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, pk=user_id)
        if request.user == target:
            return Response({"detail": "Cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.unfollow(target)
        return Response({"detail": f"You have unfollowed {target.username}."}, status=status.HTTP_200_OK)

class UserFollowersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        serializer = UserPublicSerializer(user.followers.all(), many=True, context={'request': request})
        return Response(serializer.data)

class UserFollowingAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        serializer = UserPublicSerializer(user.following.all(), many=True, context={'request': request})
        return Response(serializer.data)
 
