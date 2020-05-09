from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    due = models.DateField(null=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def is_past_due(self):
        today = now().date()
        return today > self.due

    def days_left(self):
        today = now().date()
        return today - self.due


class GoPlayer(models.Model):
    """
    An instant of Go Player
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    nick = models.CharField(max_length=20)
    total_score = models.FloatField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)

    def __str__(self):
        return self.nick

    def reset(self):
        self.total_score = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0


class GoGame(models.Model):
    """
    A single Go Game
    """
    black = models.ForeignKey(GoPlayer, on_delete=models.CASCADE, related_name='player1')
    white = models.ForeignKey(GoPlayer, on_delete=models.CASCADE, related_name='player2')
    black_score = models.FloatField()
    white_score = models.FloatField()
    date = models.DateField(default=now().date())

    def __str__(self):
        return f"{self.black} vs {self.white}, {self.game_time()}"

    def game_time(self):
        if self.date == now().date():
            return 'today'
        elif self.date == (now() + timedelta(days=-1)).date():
            return 'yesterday'
        elif self.date > (now() + timedelta(days=-7)).date():
            return f"{now().date() - self.date} days ago"
        else:
            return str(self.date)

    def winner(self):
        if self.black_score > self.white_score:
            return self.black
        elif self.black_score < self.white_score:
            return self.white

    def loser(self):
        if self.black_score < self.white_score:
            return self.black
        elif self.black_score > self.white_score:
            return self.white

    def is_draw(self):
        if self.black_score == self.white_score:
            return True
        else:
            return False

    def sum_up(self):
        self.black.total_score += self.black_score
        self.white.total_score += self.white_score
        if self.winner():
            self.winner().wins += 1
        if self.loser():
            self.loser().losses += 1
        if self.is_draw():
            self.white.draws += 1
            self.black.draws += 1


