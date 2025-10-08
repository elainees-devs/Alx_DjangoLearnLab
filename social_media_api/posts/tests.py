# posts/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from posts.models import Post, Like
from notifications.models import Notification
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()


class FeedTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', password='pass')
        self.u2 = User.objects.create_user(username='u2', password='pass')
        self.post1 = Post.objects.create(author=self.u2, content='post from u2')
        self.post2 = Post.objects.create(author=self.u2, content='another post')

        # Token for u1
        self.token_u1 = Token.objects.create(user=self.u1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_u1.key)

        # u1 follows u2
        self.u1.follow(self.u2)


class LikePostTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.post = Post.objects.create(author=self.user2, content='Hello World')

        # URLs
        self.like_url = reverse('posts:like-post', args=[self.post.id])
        self.unlike_url = reverse('posts:unlike-post', args=[self.post.id])
        self.notif_url = reverse('notifications')

        # Token auth for user1
        self.token_user1 = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user1.key)
