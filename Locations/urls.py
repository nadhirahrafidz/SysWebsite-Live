from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.createLocation, name='createLocation'),
]