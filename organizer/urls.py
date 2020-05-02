from django.urls import path

from . import views

app_name = 'organizer'

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.tasks, name='tasks'),
    path('planner/', views.planner, name='planner')
]
