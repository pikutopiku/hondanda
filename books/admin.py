from django.contrib import admin
from .models import User, Book, Hondana, Emotion, Dialog, Conf

# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Hondana)
admin.site.register(Emotion)
admin.site.register(Dialog)
admin.site.register(Conf)
