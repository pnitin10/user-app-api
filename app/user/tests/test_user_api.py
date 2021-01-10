from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
# TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)."""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'username': 'testtest',
            'email': 'test@test.com',
            'phone_number': '9876543210',
            'password': 'Te0#_-'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

#     def test_user_exists(self):
#         """Test creating a user that already exists fails"""
#         payload = {'username': 'testtest', 'password': 'test@1234'}
#         create_user(**payload)
#
#         res = self.client.post(CREATE_USER_URL, payload)
#
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_password_too_short(self):
#         """Test that the passwod must be of length 6 characters"""
#         payload = {'username': 'testtest', 'password': 'test'}
#         res = self.client.post(CREATE_USER_URL, payload)
#
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         user_exists = get_user_model().objects.filter(
#             username=payload['username']
#         ).exists()
#         self.assertFalse(user_exists)
#
#     def test_retrieve_user_unauthorized(self):
#         """Test that authentication is required for users"""
#         res = self.client.get(ME_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class PrivateUserApiTests(TestCase):
#     """Test API requests that require authentication"""
#
#     def setUp(self):
#         self.user = create_user(
#             username='testtest',
#             email='test@test.com',
#             password='Te_12@',
#             phone_number='9876543210'
#         )
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#
#     def test_retrieve_profile_success(self):
#         """Test retrieving profile for logged in user"""
#         res = self.client.get(ME_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, {
#             'username': self.user.username,
#             'email': self.user.email,
#             'phone_number': self.user.phone_number
#         })
#
#     def test_post_me_not_allowed(self):
#         """Test that POST is not allowed on the me url"""
#         res = self.client.post(ME_URL, {})
#
#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     def test_update_user_profile(self):
#         """Test updating the user profile for authenticated user"""
#         payload = {'username': 'new name', 'password': 'te_34@'}
#
#         res = self.client.patch(ME_URL, payload)
#
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.username, payload['username'])
#         self.assertTrue(self.user.check_password(payload['password']))
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
