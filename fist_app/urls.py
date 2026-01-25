from django.urls import path
from . import views

urlpatterns=[
    path('get_students',views.get_students,name='get_students'),
    path('get_students/<int:student_id>',views.get_student,name='get_student'),
    path('creat', views.create_student, name='create_student'),
    path('delete/<int:pk>',views.delete_student,name='delete_student'),
    path('update/<int:pk>',views.update_student,name='update_student'),


]