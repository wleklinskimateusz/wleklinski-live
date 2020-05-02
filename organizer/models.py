from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=User.objects.last())
    due = models.DateField(null=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title
