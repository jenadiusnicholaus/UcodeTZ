from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.conf import settings
from django.db.models.signals import post_save
from django.utils import timezone

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise TypeError('users must have email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if password is None:
            raise TypeError('Superuser must have a password')
        user = self.create_user(email, password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=16, unique=True, blank=True, null=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    enable_authenticator = models.BooleanField(default=False)  # We can use this to enable 2fa for users
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.email

    def get_short_name(self):
        return self.username


class UserProfile(models.Model):
    profile_pic = models.ImageField(upload_to='profile_picture', null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profession = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=200, choices=GENDER, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200,null=True, blank=True)
    facebook = models.URLField(null=True)
    tweeter = models.URLField(null=True)
    instagram = models.URLField(null=True)
    linkedin = models.URLField(null=True)

    def __str__(self):
        return str(self.user)

    # def first_char(self):
    #     return self.user.username[0]


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
