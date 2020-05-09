from .models import *
import django.forms as forms


class DateInput(forms.DateInput):
    input_type = 'date'


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['is_done', 'owner']
        widgets = {
            'due': DateInput(),
        }


class GoPlayerForm(forms.ModelForm):
    class Meta:
        model = GoPlayer
        fields = ['nick']


class GoGameForm(forms.Form):
    black = forms.ModelChoiceField(GoPlayer.objects.all())
    white = forms.ModelChoiceField(GoPlayer.objects.all())
    black_score = forms.FloatField()
    white_score = forms.FloatField()
    date = models.DateField(default=now().date())
