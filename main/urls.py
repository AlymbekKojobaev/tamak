from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('main/', views.index, name='main'),
    path('about/', views.about, name='about'),
]


