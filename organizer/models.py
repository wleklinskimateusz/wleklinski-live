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
    ranking = models.FloatField(default=0)

    def __str__(self):
        return self.nick

    def reset(self):
        self.total_score = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0

    def add_stats(self, points, win, draw, diff_points):
        self.total_score += points
        if win:
            self.wins += 1
            self.ranking += diff_points
        elif draw:
            self.draws += 1
        else:
            self.losses += 1
            self.ranking -= diff_points / 2

    def place(self):
        players = list(GoPlayer.objects.all().order_by('ranking'))
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
        :return: datetime.date
        """
        if self.date == localtime(now()).date():
            return 'today'
        elif self.date == (localtime(now()) + timedelta(days=-1)).date():
            return 'yesterday'
        elif self.date > (localtime(now()) + timedelta(days=-7)).date():
            return f"{(localtime(now()).date() - self.date).days} days ago"
        else:
            return self.date

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
        white.add_stats(self.white_score, self.white == self.winner(), self.is_draw(), abs(self.white_score-self.black_score))
        white.save()

        black = GoPlayer.objects.get(id=self.black.id)
        black.add_stats(self.black_score, self.black == self.winner(), self.is_draw(), abs(self.white_score-self.black_score))
        black.save()


class Trip(models.Model):
    """
    An instance for a single trip
    """
    destination = models.CharField(max_length=50)
    person1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    person2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='p2')
    person3 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='p3')
    person4 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='p4')
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    duration = models.IntegerField(null=True)
    transport = models.CharField(max_length=50, default='car')
    expected_distance = models.IntegerField(null=True, blank=True)
    fuel_cost = models.FloatField(null=True, blank=True)
    fuel_consumption = models.FloatField(null=True, blank=True)
    plane_ticket_per_person = models.FloatField(null=True, blank=True)
    train_ticket_per_person = models.FloatField(null=True, blank=True)
    total_cost = models.FloatField(default=0, blank=True)
    cost_per_person = models.FloatField(default=0, blank=True)


    def __str__(self):
        output = f"{self.destination}"
        people = self.members()
        if len(people) > 1:
            output += " with"
            for person in people:
                if not person == self.person1:
                    output += f" {person.first_name}  and"
            if output[-3:] == "and":
                output = output[:-3]
            if output[-4:] == "with":
                output = output[:-4]
        return output

    def members(self):
        """
        :return: a list of members (user objects)
        """
        lst = [self.person1]
        if self.person2:
            lst.append(self.person2)
        if self.person3:
            lst.append(self.person3)
        if self.person4:
            lst.append(self.person4)
        return lst

    def sum_up_cost(self):
        my_trip = Trip.objects.get(pk=self.id)
        my_trip.total_cost = 0
        my_trip.cost_per_person = 0
        costs = TripCost.objects.filter(trip=my_trip)
        for cost in costs:
            if cost.one_person_cost:
                my_trip.total_cost += cost.cost * len(my_trip.members())
            else:
                my_trip.cost_per_person += cost.cost
        if my_trip.transport == "car" and my_trip.fuel_consumption and my_trip.expected_distance:
            fuel = my_trip.fuel_consumption * my_trip.expected_distance / 100
            fuel_cost = fuel * my_trip.fuel_cost
            my_trip.total_cost += fuel_cost
        if my_trip.transport == "plane" and my_trip.plane_ticket_per_person:
            my_trip.total_cost += my_trip.plane_ticket_per_person * len(my_trip.members())
        if my_trip.transport == "train" and my_trip.train_ticket_per_person:
            my_trip.total_cost += my_trip.train_ticket_per_person * len(my_trip.members())

        my_trip.cost_per_person = my_trip.total_cost / len(my_trip.members())
        my_trip.save()


class TripCost(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    cost = models.FloatField()
    one_person_cost = models.BooleanField(default=False)

