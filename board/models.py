from django.db import models
from accounts.models import User


# Create your models here.
class Board(models.Model):
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    name = models.CharField('상품명(내부용)', max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('수정날짜', auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_article')
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    subject = models.CharField('제목', max_length=100)
    content = models.TextField('내용')
    is_blind = models.BooleanField('공개 여부', default=False)
    voter = models.ManyToManyField(User, related_name='voter_article')
    writer = models.CharField('글쓴이', max_length=100)
    def count_voter_user(self):
        return self.voter.count()

    def __str__(self):
        return self.subject


class Comment(models.Model):
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('수정날짜', auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    content = models.TextField('내용')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    is_modify = models.BooleanField('수정 가능 여부', default=False)
    voter = models.ManyToManyField(User, related_name='voter_comment')
    def __str__(self):
        return self.content
