from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Task)
admin.site.register(GoPlayer)
admin.site.register(GoGame)
admin.site.register(Trip)
admin.site.register(TripCost)
admin.site.register(LearningGoal)
admin.site.register(Subject)
