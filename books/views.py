from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def book_list(request):
    return render(request, 'books/book_list.html')


def hasire(request):
    return render(request, 'books/hasire.html')
