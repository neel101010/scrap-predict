from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('about/', views.about),
    path('analyse/', views.analyse),
    path('analyse/<str:company>', views.info),
    path('analyse/check/<str:company>', views.cal),
    path('methodology/', views.methodology),
]
