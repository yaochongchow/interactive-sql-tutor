from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class RegisterAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('register_user')
        self.default_data = {
            "email": "testuser@example.com",
            "name": "Test User",
            "password": "password123",
            "verify_password": "password123",
            "role": "Student"
        }

    def test_register_success(self):
        response = self.client.post(self.url, self.default_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.default_data['email']).exists())
        self.assertEqual(response.data["message"], "User registered successfully!")

    def test_password_mismatch(self):
        data = self.default_data.copy()
        data["verify_password"] = "wrongpass123"
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Passwords do not match", str(response.data))

    def test_missing_fields(self):
        data = {}  # empty dict
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)

    def test_invalid_email_format(self):
        data = self.default_data.copy()
        data["email"] = "not-an-email"
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Enter a valid email address", str(response.data))

    def test_duplicate_email(self):
        # 1st register
        self.client.post(self.url, self.default_data, format='json')
        # 2nd register with same email
        response = self.client.post(self.url, self.default_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_default_role(self):
        data = self.default_data.copy()
        data.pop("role")
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=data["email"])
        self.assertEqual(user.role, "Student")

class AuthAPITest(APITestCase):
    def setUp(self):
        # create a new account to login
        self.user = User.objects.create_user(
            email="testlogin@example.com",
            name="Test Login",
            password="testpassword123"
        )
        self.login_url = reverse('token_obtain_pair')  # login
        self.logout_url = reverse('logout')            # logout
        self.login_data = {
            "email": "testlogin@example.com",
            "password": "testpassword123"
        }

    def test_login_success(self):
        response = self.client.post(self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_fail_wrong_password(self):
        wrong_data = {
            "email": "testlogin@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_success(self):
        # login first
        login_res = self.client.post(self.login_url, self.login_data, format='json')
        access_token = login_res.data['access']
        refresh_token = login_res.data['refresh']

        # attach access token（Authorization: Bearer xxx）
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # logout（POST refresh token）
        response = self.client.post(self.logout_url, {"refresh": refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_fail_no_token(self):
        response = self.client.post(self.logout_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_logout_fail_invalid_token(self):
        # login to get Authorization header
        login_res = self.client.post(self.login_url, self.login_data, format='json')
        access_token = login_res.data['access']

        # attach access token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # use wrong refresh token
        response = self.client.post(self.logout_url, {"refresh": "invalid_token"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)