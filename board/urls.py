from django.urls import path, include
from . import views
app_name = 'board'

urlpatterns = [
    path('<int:board_id>/', views.category, name='category'),
    path('<int:board_id>/article/<int:article_id>/', views.article_detail, name='detail'),
    path('<int:board_id>/article/<int:article_id>/comment/write/', views.comment_write, name='comment_write'),
    path('<int:board_id>/article/<int:article_id>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:board_id>/write/', views.article_write, name='write'),
    path('<int:article_id>/modify/', views.article_modify, name='modify'),
    path('<int:article_id>/delete/', views.article_delete, name='delete'),
    path('article/like/', views.article_like, name='article_like')

]