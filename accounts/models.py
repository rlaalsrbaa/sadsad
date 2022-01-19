from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    first_name = None
    last_name = None
    name = models.CharField('이름', max_length=100)
