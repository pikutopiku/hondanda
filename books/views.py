from django.shortcuts import render

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView  # データ呼び出し
from . import forms

from django.http import HttpResponse
from .models import Bookshelf


from django.views.generic import CreateView
# from django.contrib.auth.forms import UserCreationForm  # 追記
from django.urls import reverse_lazy


# Create your views here.


def book_list(request):
    data = Bookshelf.objects.all()
    params = {'data': data, }
    return render(request, 'books/book_list.html', params)


def hasire(request):
    return render(request, 'books/hasire.html')

# データ呼び出し


# ログイン関係
class loginView(LoginView):
    form_class = forms.LoginForm
    template_name = "books/login.html"


class logoutView(LoginRequiredMixin, LogoutView):
    template_name = "books/logout.html"


class indexView(TemplateView):
    template_name = "books/index.html"


# アカウント作成


class createView(CreateView):
    form_class = forms.UserCreationForm
    template_name = "books/create.html"
    success_url = reverse_lazy("login")
