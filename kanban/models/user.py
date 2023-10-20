from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, phone=None, password=None, is_staff=False, is_superuser=False, is_active=True,
                    **extra_fields):
        user = self.model(
            phone=phone,
            password=password,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone=None, password=None, **extra_fields):
        return self.create_user(phone, password, is_staff=True, is_superuser=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=200)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"

    def __str__(self):
        return f"{self.phone}"


class OTP(models.Model):
    key = models.CharField(max_length=1024)
    phone = models.CharField(max_length=20)

    is_expired = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    tries = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.tries >= 3:
            self.is_expired = True

        super(OTP, self).save(*args, **kwargs)
