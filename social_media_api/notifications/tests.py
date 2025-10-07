from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from posts.models import Post
from notifications.models import Notification
from notifications.utils import create_notification

User = get_user_model()

class NotificationTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.post = Post.objects.create(author=self.user2, content='Hello World')
        self.url = reverse('notifications')
        self.client.login(username='user2', password='pass123')

    def test_create_notification(self):
        """Test creating a notification via helper"""
        create_notification(actor=self.user1, recipient=self.user2, verb='liked your post', target=self.post)
        self.assertEqual(Notification.objects.count(), 1)
        notif = Notification.objects.first()
        self.assertEqual(notif.recipient, self.user2)
        self.assertEqual(notif.actor, self.user1)
        self.assertEqual(notif.verb, 'liked your post')

    def test_fetch_notifications(self):
        """Test fetching notifications for a user"""
        create_notification(actor=self.user1, recipient=self.user2, verb='liked your post', target=self.post)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['verb'], 'liked your post')
