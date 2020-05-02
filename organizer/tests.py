from django.test import TestCase
from django.utils import timezone

import datetime

from .models import Task

# Create your tests here.


class TaskViewTests(TestCase):
    def test_past_due(self):
        """
        If task is past due should return True
        """
        yesterday = (timezone.now() + datetime.timedelta(days=-1)).date()
        past_task = Task(title='past', due=yesterday)
        self.assertIs(past_task.is_past_due(), True)

    def test_not_past_due(self):
        """
        If task is not past due should return False
        """
        tomorrow = (timezone.now() + datetime.timedelta(days=1)).date()
        future_task = Task(title='future', due=tomorrow)
        self.assertIs(future_task.is_past_due(), False)

