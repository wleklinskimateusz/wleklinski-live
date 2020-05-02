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
        form.initial['owner'] = request.user
        if form.is_valid():
            new_task = Task()
            new_task.title = form.cleaned_data['title']
            new_task.description = form.cleaned_data['description']
            new_task.owner = request.user
            new_task.due = form.cleaned_data['due']
            new_task.is_done = False
            new_task.save()
            return HttpResponseRedirect('/tasks')
    else:
        form = TaskForm()

    return render(request, template_name, {
        'form': form,
        'tasks': Task.objects.filter(owner=request.user),
    })


def planner(request):
    template_name = 'planner.html'
    return render(request, template_name, {})