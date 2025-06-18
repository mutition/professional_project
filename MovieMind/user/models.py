from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # 添加自定义字段
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    introduce = models.TextField(blank=True, null=True)
    tag = models.JSONField(blank=True, null=True)




