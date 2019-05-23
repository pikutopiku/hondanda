from django.urls import path
from . import views


urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('hasire', views.hasire, name='hasire'),
    path('login/', views.loginView.as_view(), name="login"),
    path('logout/', views.logoutView.as_view(), name="logout"),
    path('index/', views.indexView.as_view(), name="index"),
]
