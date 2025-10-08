from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from accounts.models import CustomUser
from posts.models import Post
from notifications.utils import create_notification

class NotificationTests(APITestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='user1', password='pass12345')
        self.user2 = CustomUser.objects.create_user(username='user2', password='pass12345')
        self.post = Post.objects.create(author=self.user2, content="Hello World")

        # Create token for user2 (the one fetching notifications)
        self.token = Token.objects.create(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.notifications_url = reverse('notifications')

    def test_create_notification(self):
        create_notification(actor=self.user1, recipient=self.user2, verb='liked your post', target=self.post)
        self.assertEqual(self.user2.notifications.count(), 1)

    def test_fetch_notifications(self):
        create_notification(actor=self.user1, recipient=self.user2, verb='liked your post', target=self.post)

        response = self.client.get(self.notifications_url)
        self.assertEqual(response.status_code, 200)   
