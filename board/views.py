# Create your views here.
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import ArticleForm, CommentForm
from board.models import Board, Article, Comment
from accounts.models import User


def category(request: HttpRequest, board_id):
    return article_list(request, board_id)


def article_list(request: HttpRequest, board_id):
    board = get_object_or_404(Board, id=board_id)

    kw = request.GET.get('kw', '')
    page = request.GET.get('page', '1')  # 페이지
    if not kw:
        article_list = Article.objects.filter(board=board.id).order_by('-id')

    else:
        article_list = Article.objects.filter(board=board.id, ).filter(
            Q(subject__icontains=kw) | Q(content__icontains=kw)).order_by('-id')

    paginator = Paginator(article_list, 20)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'article_list': page_obj,
               'board': board,
               }
    return render(request, 'board/article_list.html', context)


def article_detail(request: HttpRequest, board_id, article_id):
    article = get_object_or_404(Article, id=article_id)
    board = get_object_or_404(Board, id=article.board_id)
    comment = Comment.objects.filter(article_id=article_id)

    kw = request.GET.get('kw', '')
    page = request.GET.get('page', '1')  # 페이지
    if not kw:
        article_list = Article.objects.filter(board=board.id).order_by('-id')

    else:
        article_list = Article.objects.filter(board=board.id, ).filter(
            Q(subject__icontains=kw) | Q(content__icontains=kw)).order_by('-id')

    paginator = Paginator(article_list, 20)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'article': article,
               'board': board,
               'comment': comment,
               'article_list': page_obj}
    return render(request, 'board/article_detail.html', context)


@login_required
def article_write(request: HttpRequest, board_id):
    if request.user.is_authenticated:
        board = Board.objects.get(id=board_id)
        returnUrl = f"/board/{board.id}"
        if request.method == 'POST':
            form = ArticleForm(request.POST, board_id)
            if form.is_valid():
                article = form.save(commit=False)
                article.board_id = board.id
                article.user_id = request.user.id
                article.writer = request.user.username

                article.save()
                return redirect(returnUrl)
        else:
            form = ArticleForm()
        context = {'form': form,
                   'board': board}
        return render(request, 'board/article_form.html', context)
    else:
        return redirect('accounts:login')


@login_required
def article_modify(request: HttpRequest, article_id):
    article = get_object_or_404(Article, id=article_id)
    board_id = article.board_id
    board = get_object_or_404(Board, id=board_id)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "질문이 수정되었습니다.")
            return redirect(f"/board/{board_id}")
    else:
        form = ArticleForm(None, instance=article)

    return render(request, "board/article_form.html", {
        "form": form,
        "board": board,
    })


@login_required
def article_delete(request: HttpRequest, article_id):
    article = get_object_or_404(Article, id=article_id)
    board_id = article.board_id
    article.delete()
    messages.success(request, "질문이 삭제되었습니다.")
    return redirect(f"/board/{board_id}")


@login_required
def comment_write(request: HttpRequest, board_id, article_id):
    board = get_object_or_404(Board, id=board_id)
    article = get_object_or_404(Article, id=article_id)

    if request.user.is_authenticated:
        returnUrl = f"/board/{article.board_id}/article/{article.id}/"
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article_id = article.id
                comment.user_id = request.user.id
                comment.save()
                return redirect(returnUrl)
        else:
            form = CommentForm()
        context = {'form': form,
                   'board': board,
                   'article': article,
                   }
        return render(request, 'board/article_detail.html', context)
    else:
        return redirect('accounts:login')


@login_required
def comment_delete(request: HttpRequest, board_id, article_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    board_id = comment.article.board_id
    comment.delete()
    messages.success(request, "댓글이 삭제되었습니다.")
    return redirect(f"/board/{board_id}/article/{article_id}/")


@login_required
@require_POST
def article_like(request):
    pk = request.POST.get('pk', None)
    article = get_object_or_404(Article, pk=pk)
    user = request.user

    if request.user == article.user:
        return request

    if article.voter.filter(id=user.id).exists():
        article.voter.remove(user)
    else:
        article.voter.add(user)

    context = {'likes_count': article.count_voter_user()}
    return HttpResponse(json.dumps(context), content_type="application/json")
