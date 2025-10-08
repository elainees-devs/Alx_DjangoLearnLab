from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import CustomUser

class AccountsAPITests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        self.test_password = "StrongPass123"   # ✅ strong enough for validate_password
        self.user2 = CustomUser.objects.create_user(
            username='user2',
            email='user2@example.com',
            password=self.test_password
        )

    def authenticate(self):
        reg_data = {
            "username": "user1",
            "email": "user1@example.com",
            "password": self.test_password,
            "password2": self.test_password,   # ✅ include password2
            "first_name": "User",
            "last_name": "One"
        }
        reg_response = self.client.post(self.register_url, reg_data)
        self.assertEqual(reg_response.status_code, 201, reg_response.data)

        login_response = self.client.post(self.login_url, {
            "username": "user1",
            "password": self.test_password
        })
        token = login_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")


    def test_register_user(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "New",
            "last_name": "User"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 201, response.data)
        self.assertIn("user", response.data)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user"]["username"], "newuser")


    def test_login_user(self):
        CustomUser.objects.create_user(
            username="loginuser",
            email="login@example.com",
            password="pass12344"
        )
        response = self.client.post(self.login_url, {
            "username": "loginuser",
            "password": "pass12344"
        })
        self.assertEqual(response.status_code, 200, response.data)
        self.assertIn("token", response.data)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["username"], "loginuser")

    def test_get_profile(self):
        self.authenticate()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["username"], "user1")

    def test_follow_user(self):
        self.authenticate()
        url = reverse("follow-user", args=[self.user2.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200, response.data)
        self.user2.refresh_from_db()
        self.assertTrue(
            CustomUser.objects.get(username="user1") in self.user2.followers.all()
        )

    def test_unfollow_user(self):
        self.authenticate()
        # follow first
        url_follow = reverse("follow-user", args=[self.user2.id])
        self.client.post(url_follow)
        # then unfollow
        url_unfollow = reverse("unfollow-user", args=[self.user2.id])
        response = self.client.post(url_unfollow)
        self.assertEqual(response.status_code, 200, response.data)
        self.user2.refresh_from_db()
        self.assertFalse(
            CustomUser.objects.get(username="user1") in self.user2.followers.all()
        )
