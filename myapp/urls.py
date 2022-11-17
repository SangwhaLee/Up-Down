from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gameover/<int:score>', views.gameover, name='gameover'),
    path('gameclear/',views.gameclear, name='gameclear'),
    path('scoreboard/',views.scoreboard, name='scoreboard')
]
