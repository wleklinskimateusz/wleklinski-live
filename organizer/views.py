from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from .forms import TaskForm
from .models import Task
# Create your views here.


def home(request):
    template_name = 'home.html'
    return render(request, template_name, {})


def tasks(request):
    template_name = 'tasks.html'
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.owner(owner=request.user)
            form.save()
            return HttpResponseRedirect('/tasks')
    else:
        form = TaskForm()

    return render(request, template_name, {
        'form': form,
        'tasks': Task.objects.all(),
    })


def planner(request):
    template_name = 'planner.html'
    return render(request, template_name, {})