from django.shortcuts import render
from .models import *

# Create your views here.


def main(request):
    template_name = 'main.html'
    context = {
        'education': Education.objects.all(),
    }
    return render(request, template_name, context)