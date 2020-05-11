from django.urls import path

from . import views

app_name = 'organizer'

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.tasks, name='tasks'),
    path('go/', views.go_games, name='go'),
    path('go/new_player', views.new_player, name='new_player'),
    path('go/new_game', views.new_game, name='new_game'),
    path('go/games/<int:game_id>', views.go_game, name='game'),
    path('go/games/<int:pk>/delete', views.GameDeleteView.as_view(), name='delete'),
    path('go/players/<int:player_id>', views.go_player, name='player'),
]
