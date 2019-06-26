from django.shortcuts import render

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView  # データ呼び出し
from . import forms

from .models import Bookshelf, Book, TitleList, AuthorList, User
from django.views.generic import CreateView
from django.urls import reverse_lazy

import urllib.request
import urllib.error
from bs4 import BeautifulSoup


"""
import csv
from os import path
"""

# Create your views here.


def book_list(request):
    user = request.user.id
    data = Bookshelf.objects.filter(user_id=user)
    print(user)
    if (request.method == 'POST'):
        d = request.POST.get('url')

        html = urllib.request.urlopen(url=d)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find(class_='title').string
        author = soup.find(class_='author').string
        params = {'data': data, 'title': title,
                  'author': author, }
        a_num = d.find('cards') + 6
        s_num = d.find('files/')
        m_num = d.find('_')
        e_num = d.find('.html')
        author_num = d[a_num:s_num - 1]
        title_num = d[s_num+6:m_num]
        all_num = d[m_num + 1:e_num]
        print(author_num)
        print(title_num)
        print(all_num)
        title = TitleList(id=title_num, title=title)
        title.save()
        author = AuthorList(id=author_num, author=author)
        author.save()
        book = Book(id=all_num, titlelist=TitleList(id=title_num),
                    authorlist=AuthorList(id=author_num), url=d, )
        book.save()
        bookshelf = Bookshelf(user=User(id=user),
                              book=Book(id=all_num), bookmark=0)
        bookshelf.save()

    else:
        params = {'data': data, }
    return render(request, 'books/book_list.html', params)


def hasire(request):
    return render(request, 'books/hasire.html')


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


# htmlインポート(テスト)
def post_new(request):
    d = request.POST.get('url')
    key = {"msg": d}
    return render(request, 'books/index.html', key)


def book_new(request):
    if (request.method == 'POST'):
        d = request.POST.get('url')

        html = urllib.request.urlopen(url=d)
        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.title
        title = title_tag.string
        key = {"url": d, "title": title, }
        return render(request, 'books/book_list.html', key)
    else:
        return render(request, 'books/book_list.html')
