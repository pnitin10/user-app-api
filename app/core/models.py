from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        """Creates and saves a new user."""
        if not username:
            raise ValueError('Users must have an username')
        # user = self.model(email=self.normalize_email(email), **extra_fields)
        user = self.model(username=username, email=self.normalize_email(email),
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(unique=True, max_length=8)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_regex = RegexValidator(regex=r'^[6-9]\d{9}$',
                                 message="Phone number must be entered in the \
                            format: '9876543210'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=10,
                                    blank=True)

    objects = UserManager()  # It creates a new UserManager for our object

    USERNAME_FIELD = 'username'
