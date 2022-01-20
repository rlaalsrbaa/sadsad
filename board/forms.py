from django import forms
from django_summernote.widgets import SummernoteWidget

from board.models import Article, Board, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article  # 사용할 모델
        fields = ['board', 'subject', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }
        labels = {
            'board': '게시판',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # 사용할 모델
        fields = ['content']

