from django.test import TestCase
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from users.models import User
from users.serializers import UserSerializer


class SignupViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Johnny', first_name='John', last_name='doe', phone_number='+989039257150',
                                             password='password')

    def test_valid_data(self):
        data = {'username': 'John', 'password': 'ValidPassw0rd!'}
        response = self.client.post('/users/signup/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, data)

    def test_invalid_phone(self):
        data = {'username': 'John', 'phone_number': '1111', 'password': 'ValidPassw0rd!'}
        serializer = UserSerializer(data=data)
        serializer.is_valid()
        self.assertTrue(serializer.errors)
        self.assertIn('phone_number', serializer.errors)

    def test_duplicated_phone(self):
        data = {'username': 'John', 'phone_number': '+989039257150', 'password': 'ValidPassw0rd!'}
        serializer = UserSerializer(data=data)
        serializer.is_valid()
        self.assertTrue(serializer.errors)
        self.assertIn('phone_number', serializer.errors)

    def test_invalid_password(self):
        data = {'username': 'John', 'password': 'InvalidPassword'}
        serializer = UserSerializer(data=data)
        serializer.is_valid()
        self.assertTrue(serializer.errors)
        self.assertIn('password', serializer.errors)


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='John', phone_number='+989039257150', password='Correct123!')

    def test_valid_data(self):
        data = {'username': 'John', 'password': 'InCorrect123!'}
        response = self.client.post('/users/login/', data)
        self.assertEqual(response.status_code, 401)
        self.assertIn(response.data['error'], 'Incorrect password')

    def test_not_exists_user(self):
        data = {'username' : 'John111', 'password': 'Correct123!'}
        response = self.client.post('/users/login/', data)
        self.assertIn(response.data['error'], 'User not found')
        self.assertEqual(response.status_code, 404)


class RefreshTokenViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='John', phone_number='+989039257150', password='password')
        self.access_token = AccessToken.for_user(self.user)
        self.access_token['username'] = self.user.username
        self.access_token['is_staff'] = self.user.is_staff
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token['username'] = self.user.username
        self.client.cookies['access'] = str(self.access_token)
        self.client.cookies['refresh'] = str(self.refresh_token)

    def test_with_refresh_token(self):
        response = self.client.get('/users/refresh/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Token refreshed!')

    def test_without_refresh_token(self):
        self.client.cookies.pop('refresh')
        response = self.client.get('/users/refresh/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Refresh token not found!')

    def test_with_expired_refresh_token(self):
        self.refresh_token.payload['exp'] = int(now().timestamp())
        self.client.cookies['refresh'] = str(self.refresh_token)
        response = self.client.get('/users/refresh/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Invalid or Expired refresh token!')

    def test_with_invalid_refresh_token(self):
        self.refresh_token = RefreshToken()
        self.client.cookies['refresh'] = str(self.refresh_token)
        response = self.client.get('/users/refresh/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Invalid or Expired refresh token!')
