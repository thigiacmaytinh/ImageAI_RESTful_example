from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import api_view

import datetime
from django.conf import settings


def index(request):
    args = {
        'authorized': True,
        'version' : settings.VERSION
        }
    return render(request, 'index.html' , args)