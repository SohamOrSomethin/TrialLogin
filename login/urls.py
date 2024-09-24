from django.contrib import admin
from django.urls import path,include
from login import views

urlpatterns = [
    path("",views.index,name="index"),
    path('faculty', views.faculty_login, name='faculty'),
    path('student', views.student_login, name='student'),
    path("student_success/", views.student_success, name="student_success"),
    path("teacher_success/", views.teacher_success, name="teacher_success"),
    path('show_batch_data/', views.show_batch_data, name='show_batch_data'),
    path('view_student/<str:registration_number>/', views.view_student, name='view_student'),
    path('add-student/', views.add_student, name='add_student'),
    #path('student/<str:registration_number>/<str:batch_name>/', views.view_student, name='view_student'),
]