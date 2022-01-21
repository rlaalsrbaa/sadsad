import os
import random
from io import BytesIO
from urllib.parse import urlparse
from urllib.request import urlopen
from django.contrib.auth import login
from django.contrib.auth.models import AbstractUser
from django.core.files import File
from django.db import models
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import resolve_url


# Create your models here.


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성"

    class ProviderTypeCodeChoices(models.TextChoices):
        LOCAL = "local", "로컬"
        KAKAO = "kakao", "카카오"

    first_name = None
    last_name = None
    date_joined = None

    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)

    name = models.CharField('이름', max_length=100)
    gender = models.CharField('성별', max_length=1, blank=True, choices=GenderChoices.choices)
    profile_img = models.ImageField('프로필이미지', blank=True, upload_to="accounts/profile_img/%Y/%m/%d",
                                    help_text="gif/png/jpg 이미지를 업로드해주세요.")

    provider_type_code = models.CharField('프로바이더 타입코드', max_length=20, choices=ProviderTypeCodeChoices.choices,
                                          default=ProviderTypeCodeChoices.LOCAL)
    provider_accounts_id = models.PositiveIntegerField('프로바이더 회원번호', default=0)

    @staticmethod
    def login_with_kakao(request: HttpRequest, provider_accounts_id: int, provider_accounts_nickname: str,
                         provider_accounts_thumbnail_image_url: str):
        provider_type_code = User.ProviderTypeCodeChoices.KAKAO
        qs: QuerySet = User.objects.filter(provider_type_code=provider_type_code,
                                           provider_accounts_id=provider_accounts_id)

        if not qs.exists():
            username = provider_type_code + "__" + str(provider_accounts_id)
            name = provider_accounts_nickname if provider_accounts_nickname else username
            email = ""
            password = str(random.randint(1000, 9999))

            user: User = User.objects.create_user(username=username, email=email, password=password, name=name,
                                                  provider_type_code=provider_type_code,
                                                  provider_accounts_id=provider_accounts_id)

            if provider_accounts_thumbnail_image_url:
                provider_accounts_thumbnail_image_url_parsed = urlparse(provider_accounts_thumbnail_image_url)
                provider_accounts_thumbnail_image_file_name = os.path.basename(
                    provider_accounts_thumbnail_image_url_parsed.path)

                response = urlopen(provider_accounts_thumbnail_image_url)
                io = BytesIO(response.read())
                user.profile_img.save(provider_accounts_thumbnail_image_file_name, File(io))
        else:
            user: User = qs.first()

        login(request, user)

    def profile_img_url(self):
        if self.profile_img:
            return self.profile_img.url;
        return resolve_url('pydenticon_image', data=self.username)