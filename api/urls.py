from django.conf.urls import url

from . import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^file/upload$', views.UploadFile, name='fileupload'),   
]