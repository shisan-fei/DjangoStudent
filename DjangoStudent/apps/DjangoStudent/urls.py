from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^login/', views.login),
    url(r'^show_students/', views.show_students),
    path('register/', views.register),  # 用于打开注册页面
    path('register/save', views.save),  # 输入用户名密码后交给后台save函数处理
]