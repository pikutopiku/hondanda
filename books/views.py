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
    Dialog, Emotion, Dialog_log  # データ呼び出し
from django.contrib.auth.decorators import login_required

# from datetime import datetime
from django.utils import timezone


# Create your views here.


@login_required
def book_list(request):
    user = request.user.id
    data = Bookshelf.objects.filter(user_id=user)
    # print(user)

    if (request.method == 'POST'):  # URLの送信ボタンが押された時のページ表示
        d = request.POST.get('url')
        print(d.startswith('https://www.aozora.gr.jp/'))
        if d.startswith('https://www.aozora.gr.jp/') == True:
            try:
                res = urllib.request.urlopen(d)
            except urllib.error.HTTPError as e:
                print('raise HTTPError')
                print(e.code)
                print(e.reason)
                params = {'data': data, 'alart': 2}
            else:
                html = urllib.request.urlopen(url=d)
                soup = BeautifulSoup(html, "html.parser")
                title = soup.find(class_='title').string
                author = soup.find(class_='author').string
                params = {'data': data, 'title': title,
                          'author': author, 'alart': 0}
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
                    # print("あるよ")
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

                querySet = Bookshelf.objects.filter(
                    user_id=user, book_id=all_num)

                if querySet.first() is None:

                    # 本棚テーブル登録
                    bookshelf = Bookshelf(user=User(id=user),
                                          book=Book(id=all_num))
                    bookshelf.save()
        elif(len(d) >= 1):
            params = {'data': data, 'alart': 1}
            print(d)
        else:
            params = {'data': data, 'alart': 0}

    else:  # ログインからのページ表示
        params = {'data': data, 'alart': 0}

    return render(request, 'books/book_list.html', params)


@login_required
def book_text(request, u):  # u=bookid

    user = request.user.id
    k = Book.objects.get(id=u)
    # テキストデータ取得
    url = 'books/templates/books/text/' + k.url + '.txt'
    text_data = open(url, 'r')
    text = text_data.read()
    text_data.close()
    # コメントデータ取得
    d = Dialog.objects.filter(user=User(id=user), book=Book(id=u))
    d1 = d.values_list('dialog', flat=True)
    d1 = list(d1)
    d2 = d.values_list('emotionID_id', flat=True)
    if (len(d2) > 0):
        d2 = list(d2)
        dd2 = [0]*(max(d1)+1)
        for i in range(max(d1)+1):
            apper = i in d1
            if (apper):
                dd2[i] = d2[d1.index(i)]
            else:
                dd2[i] = 'a'
        print(dd2)
        params = {'data': text, 'user': user,
                  'bookID': u, 'emo2': dd2}
    else:
        params = {'data': text, 'user': user,
                  'bookID': u}
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
        lo = request.POST.get('look')
        print(lo)
        id = f"{n}{b}{s}"
        log = Dialog.objects.filter(dialog=s, book_id=b, user_id=n)

        if not (len(log) == 0):
            log = log.get(user_id=n)
            change = log.change+1
        else:
            change = 0
        utc_nou = timezone.datetime.now()  # 現在の日時
        utc_now = timezone.now()  # utc
        print(utc_now)
        print(utc_nou)

        dialog = Dialog(id=id, dialog=s, user=User(id=n),
                        book=Book(id=b), emotionID=Emotion(id=e),
                        change=change, look=lo,)
        dialog_log = Dialog_log(id=id, dialog=s, user=User(id=n),
                                book=Book(id=b), emotionID=Emotion(id=e),
                                change=change, look=lo, created=utc_now)

        dialog.save()
        dialog_log.save()

        params = {'data2': s, }
        return render(request, 'books/book_text.html', params)
    return HttpResponse("ajax is done!")


# 感情集計
def count_emotion(request):
    if (request.method == 'GET'):
        if not (request.GET.get('Dialogid') == None):
            d = request.GET.get('Dialogid')
            b = request.GET.get('Bookid')
            u = request.GET.get('User')

            log_db = Dialog.objects.filter(dialog=d, book_id=b)

            if not (log_db.count() == 0):
                log_db = log_db.exclude(user_id=u)
                response = log_db
                # prepare for data
                datas = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                labers = ['喜び', '信頼', '恐れ', '驚き', '悲しみ',
                          '嫌悪', '怒り', '期待', '無し']
                colors = ['pink', 'palegreen', 'limegreen', 'lightcyan', 'lightskyblue',
                          'mediumorchid', 'tomato', 'orange', 'silver']

                # count
                for i in range(9):
                    k = i + 1
                    datas[i] = log_db.filter(emotionID_id=k).count()
                # Not = log_db.filter(emotionID_id=10).count()

                if (sum(datas) >= 1):
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
                    print("感情グラフを作成しました．")

                else:
                    print("感情を選択した人がいません．")
                    response = 0

                return HttpResponse(response)

            else:
                print("感情付与を行った人がいません")
                response = 0
                return HttpResponse(response)
        else:
            print("からのデータです")
            return HttpResponse()
