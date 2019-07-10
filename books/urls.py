from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('hasire', views.hasire, name='hasire'),
    path('login/', views.loginView.as_view(), name="login"),
    path('logout/', views.logoutView.as_view(), name="logout"),
    path('create/', views.createView.as_view(), name="create"),
    path('index/', views.post_new, name='post_new'),
    path('text/<str:u>', views.text, name='text'),
    # path('', views.book_new, name='book_new'),
]
