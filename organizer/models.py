from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now, localtime


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

    def add_stats(self, points, win, draw):
        self.total_score += points
        if win:
            if draw:
                self.draws += 1
            else:
                self.wins += 1
        else:
            self.losses += 1

    def ranking(self):
        players = list(GoPlayer.objects.all().order_by('total_score'))
        players.reverse()
        return players.index(self) + 1


class GoGame(models.Model):
    """
    A single Go Game
    """
    black = models.ForeignKey(GoPlayer, on_delete=models.CASCADE, related_name='player1')
    white = models.ForeignKey(GoPlayer, on_delete=models.CASCADE, related_name='player2')
    black_score = models.FloatField()
    white_score = models.FloatField()
    date = models.DateField(default=localtime(now()).date())

    def __str__(self):
        """
        It's defined here what should be displayed when mentioning the object
        :return: str
        """
        return f"{self.black} vs {self.white}, {self.game_time()}"

    def game_time(self):
        """
        time of a game with relation with today
        :return: str
        """
        if self.date == localtime(now()).date():
            return 'today'
        elif self.date == (localtime(now()) + timedelta(days=-1)).date():
            return 'yesterday'
        elif self.date > (localtime(now()) + timedelta(days=-7)).date():
            return f"{localtime(now()).date() - self.date} days ago"
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
        """
        Checks if is draw (if even possible)
        :return: bool
        """
        if self.black_score == self.white_score:
            return True
        else:
            return False

    def sum_up(self):
        white = GoPlayer.objects.get(id=self.white.id)
        white.add_stats(self.white_score, self.white == self.winner(), self.is_draw())
        white.save()

        black = GoPlayer.objects.get(id=self.black.id)
        black.add_stats(self.black_score, self.black == self.winner(), self.is_draw())
        black.save()
