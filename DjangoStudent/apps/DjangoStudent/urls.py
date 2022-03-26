from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^login/', views.login),
    url(r'^show_students/', views.show_students),
    path(r'update/', views.update_pwd),  # 用于打开密码修改页面
    path(r'update/save', views.save),  # 输入用户名密码后交给后台save函数处理
]