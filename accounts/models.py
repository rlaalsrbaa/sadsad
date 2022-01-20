from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    name = models.CharField('이름', max_length=100)
    first_name = None
    last_name = None

    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성"

    gender = models.CharField('성별', max_length=1, blank=True, choices=GenderChoices.choices)