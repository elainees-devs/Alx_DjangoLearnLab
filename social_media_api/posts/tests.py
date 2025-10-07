# posts/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from posts.models import Post, Like
from notifications.models import Notification
from notifications.utils import create_notification
from rest_framework import status

User = get_user_model()

class FeedTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', password='pass')
        self.u2 = User.objects.create_user(username='u2', password='pass')
        Post.objects.create(author=self.u2, content='post from u2')
        Post.objects.create(author=self.u2, content='another post')

    def test_feed_shows_followed_user_posts(self):
        self.client.login(username='u1', password='pass')
        # u1 follows u2
        self.u1.follow(self.u2)
        resp = self.client.get(reverse('posts:feed'))  # ensure posts/urls uses app_name='posts'
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Expect 2 posts
        self.assertEqual(len(resp.data), 2)

class LikePostTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.post = Post.objects.create(author=self.user2, content='Hello World')
        self.like_url = reverse('like-post', args=[self.post.id])
        self.unlike_url = reverse('unlike-post', args=[self.post.id])
        self.client.login(username='user1', password='pass123')

    def test_like_post(self):
        """User can like a post"""
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.first().verb, 'liked your post')

    def test_like_post_twice(self):
        """User cannot like the same post twice"""
        self.client.post(self.like_url)
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Like.objects.count(), 1)

    def test_unlike_post(self):
        """User can unlike a post they liked"""
        self.client.post(self.like_url)
        response = self.client.post(self.unlike_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.count(), 0)

    def test_unlike_post_not_liked(self):
        """Cannot unlike a post that wasn't liked"""
        response = self.client.post(self.unlike_url)
        self.assertEqual(response.status_code, 400)
