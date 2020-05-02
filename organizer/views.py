from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from .forms import TaskForm
from .models import Task
# Create your views here.


def get_tasks_to_context(context, request):

    tasks_todo = Task.objects.filter(owner=request.user, is_done=False)
    past_due = 0
    for task in tasks_todo:
        if task.is_past_due():
            past_due += 1
    context['tasks_to_do'] = len(tasks_todo)
    context['past_due'] = past_due
    return context


def home(request):
    template_name = 'home.html'

    context = get_tasks_to_context({}, request)

    return render(request, template_name, context)


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
    context = {
        'form': form,
        'tasks': Task.objects.filter(owner=request.user),
    }
    context = get_tasks_to_context(context, request)

    return render(request, template_name, context)


def planner(request):
    template_name = 'planner.html'
    context = get_tasks_to_context({}, request)
    return render(request, template_name, context)