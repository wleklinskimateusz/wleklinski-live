from . import views
from django.urls import path

app_name = 'cv'

urlpatterns = [
    path('', views.main, name='home'),
]
