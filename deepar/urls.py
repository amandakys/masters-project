# accounts/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('', views.deepar, name='deepar'),
    path('filters/', views.filters, name='filters'),
    path ('select/', views.select, name='select'),
    path('complete/', views.complete, name='complete')
]

