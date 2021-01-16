from django.urls import path
from . import views


app_name = 'teams'


urlpatterns = [
    path('', views.CookCreateView.as_view(), name='teams'),
]
