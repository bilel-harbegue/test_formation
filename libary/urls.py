from django.urls import path
from . import views

urlpatterns = [
     path('get_all_books',views.get_all_books,name='get_all_books'),
    path('get_book/<int:pk>',views.get_book,name='get_book'),
    path('delete_book/<int:pk>',views.delete_book,name='delete_book'),
    path('creat', views.create_book, name='create_book'),
    path('update',views.update_one_book,name='update_one_book'),



]
