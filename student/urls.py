
from django.contrib import admin
from django.conf.urls import url,include
from django.urls import path,re_path
from student import views



urlpatterns = [
    url(r'^$', views.index,name="stu_index"),
]
