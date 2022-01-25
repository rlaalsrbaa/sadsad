from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404

from board.models import Board, Article


def index(request: HttpRequest):
    board = Board.objects.all()
    page = request.GET.get('page', '1')  # 페이지

    notice_index = Article.objects.filter(board=1).order_by('-id')
    paginator = Paginator(notice_index, 10)  # 페이지당 10개씩 보여주기
    notice_index_page_obj = paginator.get_page(page)

    free_index = Article.objects.filter(board=2).order_by('-id')
    paginator = Paginator(free_index, 10)  # 페이지당 10개씩 보여주기
    free_index_page_obj = paginator.get_page(page)

    humor_index = Article.objects.filter(board=3).order_by('-id')
    paginator = Paginator(humor_index, 10)  # 페이지당 10개씩 보여주기
    humor_index_page_obj = paginator.get_page(page)

    animal_index = Article.objects.filter(board=4).order_by('-id')
    paginator = Paginator(animal_index, 10)  # 페이지당 10개씩 보여주기
    animal_index_page_obj = paginator.get_page(page)

    context = {'notice_index': notice_index_page_obj,
               'free_index': free_index_page_obj,
               'humor_index': humor_index_page_obj,
               'animal_index': animal_index_page_obj,
               'board': board,
               }
    return render(request, "home/main.html", context)

