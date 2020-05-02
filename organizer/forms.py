from .models import Task
import django.forms as forms
from django.contrib.admin.widgets import AdminDateWidget

class DateInput(forms.DateInput):
    input_type = 'date'


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['is_done']
        widgets = {
            'due': DateInput(),
            'owner': forms.HiddenInput()
        }
