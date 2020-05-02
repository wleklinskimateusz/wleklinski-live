from .models import Task
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

