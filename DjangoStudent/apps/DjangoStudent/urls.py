from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/', views.login),
    url(r'^show_students/', views.show_students),
]