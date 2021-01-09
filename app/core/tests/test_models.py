from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_username_successful(self):
        """Test creating a new user with an email is successful"""
        username = 'tstties'
        email = 'tetest.com'
        password = 'test@1234'
        phone_number = '9876543210'
        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=phone_number
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    # def test_new_user_email_normalized(self):
    #     """Test the email for a new user is normalized"""
    #     email = 'TEST@1234.com'
    #     user = get_user_model().objects.create_user('testtest', email,
    #                                                 'test@1234')
    #
    #     self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_username(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test@test.com',
                                                 'test@1234')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'testtest',
            'test@test.com',
            'test@1234'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
