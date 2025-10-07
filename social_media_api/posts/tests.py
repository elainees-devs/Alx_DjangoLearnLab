# posts/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from posts.models import Post
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
