from django.shortcuts import render

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from . import forms

# Create your views here.


def book_list(request):
    return render(request, 'books/book_list.html')


def hasire(request):
    return render(request, 'books/hasire.html')


class loginView(LoginView):
    form_class = forms.LoginForm
    template_name = "books/login.html"


class logoutView(LoginRequiredMixin, LogoutView):
    template_name = "books/logout.html"


class indexView(TemplateView):
    template_name = "books/index.html"
