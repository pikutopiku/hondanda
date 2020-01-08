from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('login/', views.loginView.as_view(), name="login"),
    path('logout/', views.logoutView.as_view(), name="logout"),
    path('create/', views.createView.as_view(), name="create"),
    path('book_text/<str:u>', views.book_text, name='book_text'),
    path('book_text/save_emotion/', views.seve_emotion, name='seve_emotion'),
    path('book_text/count_emotion/', views.count_emotion, name='count_emotion'),
]
