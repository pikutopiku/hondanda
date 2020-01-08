import os.path  # books/templates/books/text/にあるファイルをimport
from bs4 import BeautifulSoup
import urllib.error
import urllib.request
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from .models import Bookshelf, Book, TitleList, AuthorList, User, \
    Dialog, Emotion  # データ呼び出し
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def book_list(request):
    user = request.user.id
    data = Bookshelf.objects.filter(user_id=user)
    # print(user)

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
            pass  # あるよ
        else:
            # print("ないよ")
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

        querySet = Bookshelf.objects.filter(user_id=user, book_id=all_num)

        if querySet.first() is None:

            # 本棚テーブル登録
            bookshelf = Bookshelf(user=User(id=user),
                                  book=Book(id=all_num))
            bookshelf.save()

    else:  # ログインからのページ表示
        params = {'data': data, }

    return render(request, 'books/book_list.html', params)


@login_required
def book_text(request, u):  # u=bookid

    user = request.user.id
    k = Book.objects.get(id=u)

    url = 'books/templates/books/text/' + k.url + '.txt'
    text_data = open(url, 'r')
    text = text_data.read()
    text_data.close()
    params = {'data': text, 'user': user, 'bookID': u, }

    return render(request, 'books/book_text.html', params)


# ログイン関係
class loginView(LoginView):  # login
    form_class = forms.LoginForm
    template_name = "books/login.html"


class logoutView(LoginRequiredMixin, LogoutView):  # logout
    template_name = "books/logout.html"


# アカウント作成
class createView(CreateView):
    form_class = forms.UserCreationForm
    template_name = "books/create.html"
    success_url = reverse_lazy("login")


# 感情登録
def seve_emotion(request):
    if (request.method == 'POST'):  # POSTの受信時
        n = request.POST.get('idName')
        b = request.POST.get('bookID')
        s = request.POST.get('id')
        e = request.POST.get('radioVal')
        id = f"{n}{b}{s}"
        dialog = Dialog(id=id, dialog=s, user=User(id=n),
                        book=Book(id=b), emotionID=Emotion(id=e))
        dialog.save()

        params = {'data2': s, }
        return render(request, 'books/book_text.html', params)
    return HttpResponse("ajax is done!")


# 感情集計
def count_emotion(request):
    if (request.method == 'GET'):
        d = request.GET.get('Dialogid')
        b = request.GET.get('Bookid')
        log_db = Dialog.objects.filter(dialog=d, book_id=b)

        if not (log_db.count() == 0):
            response = log_db
            # prepare for data
            datas = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            labers = ['喜び', '信頼', '恐れ', '驚き', '悲しみ',
                      '嫌悪', '怒り', '期待', '無し']
            colors = ['pink', 'palegreen', 'limegreen', 'lightcyan', 'lightskyblue',
                      'mediumorchid', 'tomato', 'orange', 'silver']

            # count
            emo = []
            for i in range(9):
                k = i + 1
                emo = log_db.filter(emotionID_id=k,)
                datas[i] = log_db.filter(emotionID_id=k).count()

            # # create figure
            import matplotlib
            matplotlib.use('Agg')  # <= これが必要
            import matplotlib.pyplot as plt
            import matplotlib.cm as cm
            import numpy as np
            import japanize_matplotlib

            # 綺麗に書くためのおまじない###
            plt.style.use('ggplot')
            plt.rcParams.update({'font.size': 15})

            # 各種パラメータ###
            size = (6, 5)  # 凡例を配置する関係でsizeは横長にしておきます。

            # pie###
            plt.figure(figsize=size, dpi=100)
            plt.pie(datas, colors=colors, counterclock=False, startangle=90,
                    autopct=lambda p: '{:.1f}%'.format(p) if p >= 5 else '')
            plt.subplots_adjust(left=0, right=0.7)

            plt.legend(labers, fancybox=True, loc='center left',
                       bbox_to_anchor=(0.9, 0.5))
            plt.axis('equal')
            plt.savefig('books/static/figure.png',
                        bbox_inches='tight', pad_inches=0.05)

            return HttpResponse(response)

        else:
            return HttpResponse()
