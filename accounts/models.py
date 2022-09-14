from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=100, unique=True)  # id
    nickname = models.CharField(max_length=30, unique=True)  # 닉네임
    phone = models.CharField(max_length=11, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    # python manage.py createsuperuser로 사용자를 만들 때 필수로 입력하게 되는 필드 리스트
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.nickname
