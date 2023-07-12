from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^(?P<lang>[a-z]{2})?$', views.index, name='index'),
    re_path(r'^sign/$', views.sign, name='sign'),
    re_path(r'^confirm/([0-9a-z]{64})/$', views.confirm, name='confirm'),
]
