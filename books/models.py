from django.db import models

# Create your models here.


class User(models.Model):
    # ユーザー情報
    name = models.CharField(max_length=100)
    mail = models.EmailField(max_length=200)
    gender = models.BooleanField()
    age = models.IntegerField(default=0)

    def __str__(self):
        return '<User:id=' + str(self.id) + ', ' + \
            self.name + '(' + str(self.age) + ')>'


class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 書籍情報
    title = models.CharField(max_length=100)
    bookmark = models.IntegerField(default=0)

    def __str__(self):
        return '<Book:' + str(self.user.name) + ', ' + \
            self.title + '(' + str(self.bookmark) + 'ページ)>'
