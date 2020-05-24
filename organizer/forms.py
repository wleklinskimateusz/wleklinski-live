from .models import *
import django.forms as forms


def get_users():
    output = []
    for user in User.objects.all():
        output.append((user.id, user.first_name))
    return tuple(output)

def get_transport():
    return (
        ('plane', 'plane'),
        ('car', 'car'),
        ('train', 'train'),
        ('bike', 'bike')
    )


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


class TripInitForm(forms.Form):
    destination = forms.CharField(max_length=50)
    people = forms.MultipleChoiceField(choices=get_users())
    transport = forms.ChoiceField(choices=get_transport())
    duration = forms.IntegerField()
