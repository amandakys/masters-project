# experimenttwo/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('', views.camera, name='camera'),
    path('next/', views.next, name='next'),
    # path('filters/', views.filters, name='filters'),
    path ('select/', views.select, name='selectthree'),
    # path('complete/', views.complete, name='complete')
]

