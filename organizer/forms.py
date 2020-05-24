from .models import *
import django.forms as forms


def get_users():
    output = [('', "---------")]
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
    person2 = forms.ChoiceField(choices=get_users(), required=False)
    person3 = forms.ChoiceField(choices=get_users(), required=False)
    person4 = forms.ChoiceField(choices=get_users(), required=False)
    transport = forms.ChoiceField(choices=get_transport())
    duration = forms.IntegerField(label="duration [days]")


class TripEditForm(TripInitForm):
    start = forms.DateField(required=False, widget=DateInput)


class TripEditFormCar(TripEditForm):
    expected_distance = forms.IntegerField(required=False, label="Expected Distance [km]")
    fuel_cost = forms.FloatField(required=False, label='Fuel Cost [zł/l]')
    fuel_consumption = forms.FloatField(required=False, label="Fuel Consumption [l/100km]")


class TripEditFormBike(TripEditForm):
    expected_distance = forms.IntegerField(required=False)


class TripEditFormPlane(TripEditForm):
    plane_ticket_per_person = forms.FloatField(required=False)


class TripEditFormTrain(TripEditForm):
    train_ticket_per_person = forms.FloatField(required=False)