import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        """Creates and saves a new user."""
        if not username:
            raise ValueError('Users must have an username')
        if len(username) != 8:
            raise ValueError('Username max length should be 8')
        if len(password) != 6:
            raise ValueError('Password max length should be 6')
        # if bool(re.match("[A-Za-z0-9#_-]", password)):
        #     raise ValidationError(
        #         _("Password must contain at least one character, one number\
        #          and any one of these (underscore, hyphen, hash)."),
        #         code='password_no_number',
        #     )
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        """Creates and saves a new super user."""
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=8, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_regex = RegexValidator(regex=r'^[6-9]\d{9}$',
                                 message="Phone number must be entered in the \
                            format: '9876543210'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=10)

    objects = UserManager()  # It creates a new UserManager for our object

    USERNAME_FIELD = 'username'
