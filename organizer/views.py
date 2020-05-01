from django.shortcuts import render
from django.views import generic
# Create your views here.


def home(request):
    template_name = 'home.html'
    return render(request, template_name, {})