from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
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


def get_player_to_context(context, request):
    player = None
    if GoPlayer.objects.filter(owner=request.user):
        player = GoPlayer.objects.get(owner=request.user)
    context['player'] = player
    return context


def home(request):
    if not request.user.is_authenticated:
        return redirect('accounts/login')

    template_name = 'home.html'

    context = get_player_to_context({}, request)

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
        'tasks': Task.objects.filter(owner=request.user)
    }
    context = get_player_to_context(context, request)

    return render(request, template_name, context)


def go_game(request):
    template_name = 'gamesGO.html'
    context = {
        'games': GoGame.objects.all()
    }
    context = get_player_to_context(context, request)

    return render(request, template_name, context)


def new_player(request):
    template_name = 'forms/new_player.html'
    if request.method == 'POST':
        form = GoPlayerForm(request.POST)
        if form.is_valid():
            Player = GoPlayer()
            Player.owner = request.user
            Player.nick = form.cleaned_data['nick']
            Player.save()
            return HttpResponseRedirect('/go')
    else:
        form = GoPlayerForm()
    context = {
        'form': form,
    }
    context = get_player_to_context(context, request)

    return render(request, template_name, context)


def new_game(request):
    template_name = 'forms/new_game.html'
    if request.method == 'POST':
        form = GoGameForm(request.POST)
        if form.is_valid():
            game = GoGame()
            game.white = form.cleaned_data['white']
            game.black = form.cleaned_data['black']
            game.black_score = form.cleaned_data['black_score']
            game.white_score = form.cleaned_data['white_score']
            game.save()
            game.sum_up()

            return HttpResponseRedirect('/go')
    else:
        form = GoGameForm()
    context = {
        'form': form,

    }
    context = get_player_to_context(context, request)

    return render(request, template_name, context)
