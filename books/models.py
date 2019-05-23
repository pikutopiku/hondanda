from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # ユーザー情報
    pass

    def __str__(self):
        return '<user:id=' + str(self.id) + '(' + self.username + ')>'


class TitleList(models.Model):
    # タイトル情報
    id = models.IntegerField(primary_key=True)  # タイトルID
    title = models.CharField(max_length=100)  # タイトル名

    def __str__(self):
        return '<title:id=' + str(self.id) + '(' + self.title + ')>'


class AuthorList(models.Model):
    # 作者情報
    id = models.IntegerField(primary_key=True)    # 作者ID
    author = models.CharField(max_length=100)  # 作者名

    def __str__(self):
        return '<suthor:id=' + str(self.id) + '(' + self.author + ')>'


class Book(models.Model):
    # 書籍情報
    id = models.IntegerField(primary_key=True)  # 青空文庫 html_URLの後ろの番号
    titlelist = models.ForeignKey(
        TitleList, on_delete=models.CASCADE)  # TitleList関連付け
    authorlist = models.ForeignKey(
        AuthorList, on_delete=models.CASCADE)  # AuthouList関連付け

    def __str__(self):
        return '<book:id=' + str(self.id) + ',' + \
            self.titlelist.title + '(' + self.authorlist.author + ')>'


class Bookshelf(models.Model):
    # 本棚情報
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Userと関連付け
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Bookと関連付け
    bookmark = models.IntegerField(default=0)  # しおり

    def __str__(self):
        return '<Hondana:' + self.user.username + ', ' + \
            self.book.titlelist.title + '(' + str(self.bookmark) + 'ページ)>'


class Emotion(models.Model):
    # 感情情報
    emotion = models.CharField(max_length=100)  # 感情名(一時的に単語で作成)

    def __str__(self):
        return '<emotion:' + str(self.id) + '(' + self.emotion + ')>'


class Dialog(models.Model):
    # 会話情報
    id = models.IntegerField(primary_key=True, default=0)  # セリフ番号
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Userと関連付け
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Bookと関連付け
    emotionID = models.ForeignKey(
        Emotion, on_delete=models.CASCADE)  # Emotionと関連付け

    def __str__(self):
        return '<serif:' + self.user.username + ', ' + \
            self.book.titlelist.title + ', ' + str(self.id) + \
            '(' + self.emotionID.emotion + ')> '


class Conf(models.Model):
    # ユーザー設定情報
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Userと関連付け
    char = models.IntegerField(default=0)  # 文字サイズ
    color = models.CharField(max_length=100)  # 色
    way = models.BooleanField()  # 文字向き

    def __str__(self):
        return '<user:' + str(self.user.username) + ', ' + \
            'size:' + str(self.char) + ', ' + 'color:' + str(self.color) + '>'
