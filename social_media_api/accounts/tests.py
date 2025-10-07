# accounts/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class FollowTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='u1', password='pass')
        self.user2 = User.objects.create_user(username='u2', password='pass')

    def test_follow_and_unfollow(self):
        self.client.login(username='u1', password='pass')
        url_follow = reverse('accounts:follow-user', args=[self.user2.id])
        url_unfollow = reverse('accounts:unfollow-user', args=[self.user2.id])

        resp = self.client.post(url_follow)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user1.is_following(self.user2))

        resp = self.client.post(url_unfollow)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user1.is_following(self.user2))
