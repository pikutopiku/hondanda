from django.db import models

# Create your models here.


class User(models.Model):
    # ユーザー情報
    name = models.CharField(max_length=100)
    mail = models.EmailField(max_length=200)

    def __str__(self):
        return '<User:id=' + str(self.id) + ', ' + self.name + '>'


class Book(models.Model):
    # 書籍情報
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return '<book:id=' + str(self.id) + ',' + \
            self.title + '(' + self.author + ')>'


class Hondana(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    bookmark = models.IntegerField(default=0)

    def __str__(self):
        return '<Hondana:' + str(self.user.name) + ', ' + \
            self.book.title + '(' + str(self.bookmark) + 'ページ)>'


class Emotion(models.Model):
    emotion = models.CharField(max_length=100)

    def __str__(self):
        return '<emotionID:' + str(self.id) + ', ' + \
            '(' + self.emotion + ')>'


class Dialog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    serifID = models.IntegerField(default=0)
    emotionID = models.ForeignKey(Emotion, on_delete=models.CASCADE)

    def __str__(self):
        return '<serif:' + self.hondana.user.name + ', ' + \
            self.hondana.book.title + ', ' + str(self.serifID) + \
            '(' + self.emotion + ')> '


class Conf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    char = models.IntegerField(default=0)
    color = models.CharField(max_length=100)
    way = models.BooleanField()

    def __str__(self):
        return '<user:' + str(self.user.name) + ', ' + \
            'size:' + str(self.char) + ', ' + 'color:' + str(self.color) + '>'
