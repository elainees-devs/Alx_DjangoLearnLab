from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login,authenticate, logout
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer, UserPublicSerializer, LoginSerializer


User = get_user_model()


class RegisterUser(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'accounts/register.html'

    def get(self, request):
        serializer = self.get_serializer()
        return Response({'form': serializer})

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'form': serializer, 'token': serializer.get_token(user)})
        return Response({'form': serializer, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
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

class LoginUser(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'accounts/login.html'

    def get(self, request):
        serializer = self.get_serializer()
        return Response({'form': serializer})

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)  # log in the user
                token, _ = Token.objects.get_or_create(user=user)
                request.session['api_token'] = token.key  # store token in session

                # redirect to feed page (or any other page)
                return redirect('posts:feed')  

            return Response({'form': serializer, 'errors': {'non_field_errors': ['Invalid credentials']}}, 
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'form': serializer, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutUser(APIView):
        permission_classes = [IsAuthenticated]

        def get(self, request):
            logout(request)
            return redirect('accounts:login')  # redirect to login page after logout


    
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
    
class FollowUserAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        target = self.get_queryset().filter(pk=user_id).first()
        if not target:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user == target:
            return Response({"detail": "Cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.follow(target)
        return Response({"detail": f"You are now following {target.username}."}, status=status.HTTP_200_OK)


class UnfollowUserAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all() 

    def post(self, request, user_id):
        target = self.get_queryset().filter(pk=user_id).first()
        if not target:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user == target:
            return Response({"detail": "Cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.unfollow(target)
        return Response({"detail": f"You have unfollowed {target.username}."}, status=status.HTTP_200_OK)
    
class UserFollowersAPIView(generics.ListAPIView):
    """
    List all followers of a given user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserPublicSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(CustomUser, pk=user_id)
        # CustomUser model must have a 'followers' ManyToMany field
        return user.followers.all()


class UserFollowingAPIView(generics.ListAPIView):
    """
    List all users that a given user is following.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserPublicSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(CustomUser, pk=user_id)
        # 'following' is the related_name for the followers ManyToMany
        return user.following.all()


