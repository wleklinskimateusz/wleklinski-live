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
    path('trips/', views.trips, name='trips'),
    path('trips/create', views.new_trip, name='new_trip'),
    path('trips/<int:trip_id>/display', views.trip, name='trip_display'),
    path('trips/<int:trip_id>/edit', views.trip_edit, name='trip_edit'),
    path('trips/<int:trip_id>/finances', views.trip_finances, name='trip_finances'),
    path('trips/<int:trip_id>/finances/new_cost', views.new_cost, name='new_cost'),
    path('learning/', views.learning, name='learning'),
    path('learning/<int:goal_id>/update', views.learning_update, name='learning_update'),
]
