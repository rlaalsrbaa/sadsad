from django import forms
from board.models import Article, Board, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article  # 사용할 모델
        fields = ['board', 'subject', 'content']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'board': forms.Select
        }
        labels = {
            'board': '게시판',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # 사용할 모델
        fields = ['content']

