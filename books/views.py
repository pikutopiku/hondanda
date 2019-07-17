from django.shortcuts import render

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from . import forms

from .models import Bookshelf, Book, TitleList, AuthorList, User  # データ呼び出し
from django.views.generic import CreateView
from django.urls import reverse_lazy

import urllib.request
import urllib.error
from bs4 import BeautifulSoup

import os.path

from xml.sax.saxutils import unescape


# Create your views here.


def book_list(request):
    user = request.user.id
    data = Bookshelf.objects.filter(user_id=user)
    print(user)

    if (request.method == 'POST'):  # URLの送信ボタンが押された時のページ表示
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
        f_name = d[s_num+6:e_num]

        # 作品名，ID登録
        title = TitleList(id=title_num, title=title)
        title.save()

        # 著者名，ID登録
        author = AuthorList(id=author_num, author=author)
        author.save()

        # 　本文ファイル保存
        s1 = 'books/templates/books/text/' + f_name + '.txt'
        if os.path.isfile(s1) is True:
            print("あるよ")
        else:
            print("ないよ")
            head_tag = soup.head.prettify()
            body_tag = soup.body.prettify()
            html_tag = head_tag + body_tag
            f = open(s1, 'w')
            f.write(html_tag)
            f.close()

        # Bookテーブル登録
        book = Book(id=all_num, titlelist=TitleList(id=title_num),
                    authorlist=AuthorList(id=author_num), url=f_name, )
        book.save()

        # 本棚テーブル登録
        bookshelf = Bookshelf(user=User(id=user),
                              book=Book(id=all_num), bookmark=0)
        bookshelf.save()

    else:  # ログインからのページ表示
        params = {'data': data, }

    return render(request, 'books/book_list.html', params)


def hasire(request):
    return render(request, 'books/hasire.html')


def book_text(request, u):
    url = 'books/templates/books/text/' + u + '.txt'
    text_data = open(url, 'r')
    text = text_data.read()
    text_data.close()
    params = {'data': text, }
    return render(request, 'books/book_text.html', params)


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
