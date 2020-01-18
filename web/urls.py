from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^404/$', views.notfound, name='notfound'),
]
handler404 = views.notfound
