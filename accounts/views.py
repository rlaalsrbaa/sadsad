from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from .decorators import logout_required

# Create your views here.
from accounts.forms import SignupForm

@logout_required
def login(request: HttpRequest):
    return LoginView.as_view(template_name="accounts/login.html")(request)

@logout_required
def signup(request: HttpRequest):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request, "회원가입 환영합니다.")
            # signed_user.send_welcome_email()  # FIXME: Celery로 처리하는 것을 추천.
            next_url = request.GET.get('next', '/')
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {
        'form': form,
    })