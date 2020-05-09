from django.urls import path

from . import views

app_name = 'organizer'

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.tasks, name='tasks'),
    path('go/', views.go_game, name='go'),
    path('forms/new_player', views.new_player, name='new_player'),
    path('forms/new_game', views.new_game, name='new_game')
]
