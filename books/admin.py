from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TitleList,  AuthorList, Book, Bookshelf, \
    Emotion, Dialog, Conf, Dialog_log


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(TitleList)
admin.site.register(AuthorList)
admin.site.register(Book)
admin.site.register(Bookshelf)
admin.site.register(Emotion)
admin.site.register(Dialog)
admin.site.register(Dialog_log)
admin.site.register(Conf)
