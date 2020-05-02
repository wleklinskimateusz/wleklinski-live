from django.shortcuts import render
from django.views import generic
# Create your views here.


def home(request):
    template_name = 'home.html'
    return render(request, template_name, {})


def tasks(request):
    template_name = 'tasks.html'
    return render(request, template_name, {})


def planner(request):
    template_name = 'planner.html'
    return render(request, template_name, {})