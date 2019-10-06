
from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url,include
from crm import views
urlpatterns = [
    url(r'^$', views.index,name="sales_index"),
    url(r'^tpl1/', views.tpl1),
    url(r'^tpl2/', views.tpl2),
    url(r'^tpl3/', views.tpl3),
    url(r'^tpl4/', views.tpl4),
    re_path('^customers/$', views.customer_list,name="customer_list"),

]
