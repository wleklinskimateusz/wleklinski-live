from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from django.urls import reverse_lazy, reverse
# Create your views here.


def get_player_to_context(context, request):
    """
    :param context: takes old context
    :param request: request from the user
    :return: return new context with player added
    """
    player = None
    if GoPlayer.objects.filter(owner=request.user):
        player = GoPlayer.objects.get(owner=request.user)
    context['Iplayer'] = player
    return context


def home(request):
    """
    Home Page View
    :param request:
    :return: renders a HTML page
    """
    if not request.user.is_authenticated:
        return redirect('accounts/login')

    template_name = 'home.html'

    context = get_player_to_context({}, request)

    return render(request, template_name, context)


def tasks(request):
    """
    Tasks Page View
    :param request:
    :return: renders a page
    """

    if not request.user.is_authenticated:
        return redirect('/accounts/login')

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


def go_games(request):
    """
    Go Games General View
    :param request:
    :return: renders a page
    """

    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'go/gamesGO.html'
    context = {
        'games': GoGame.objects.all().order_by('-id'),
        'players': reversed(list(GoPlayer.objects.all().order_by('ranking')))
    }
    context = get_player_to_context(context, request)

    return render(request, template_name, context)


def new_player(request):
    """
    a Form to create a new player
    :param request:
    :return: renders a form
    """

    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'forms/default.html'
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
        'title': "New Player"
    }
    context = get_player_to_context(context, request)

    return render(request, template_name, context)


def new_game(request):
    """
    A Form to add new game
    :param request:
    :return: renders a form
    """

    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'forms/default.html'
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
        'title': "New Game"

    }
    context = get_player_to_context(context, request)

    return render(request, template_name, context)


def go_game(request, game_id):
    """
    Displays detailed view of a particular game
    :param request:
    :param game_id: particular game id
    :return: renders a page
    """
    my_game = get_object_or_404(GoGame, pk=game_id)
    if my_game.white.owner == request.user:
        player = my_game.white
        player_score = my_game.white_score

        opponent = my_game.black
        opponent_score = my_game.black_score
    else:
        player = my_game.black
        player_score = my_game.black_score

        opponent = my_game.white
        opponent_score = my_game.white_score
    template_name = 'go/game.html'
    context = {
        'opponent': opponent,
        'player': player,
        'player_score': player_score,
        'opponent_score': opponent_score,
        'win': my_game.winner().owner == request.user,
        'id': my_game.id
    }
    context = get_player_to_context(context, request)
    return render(request, template_name, context)


def go_player(request, player_id):
    """
    Displays detailed view of a player
    :param request:
    :param player_id:
    :return: renders a page
    """
    player = get_object_or_404(GoPlayer, pk=player_id)
    template_name = 'go/player.html'
    played_with_me = 0
    for game in GoGame.objects.all():
        if (game.white == player and game.black.owner == request.user) or (game.black == player and game.white.owner == request.user):
            played_with_me += 1
    context = {
        'player': player,
        'played_with_me': played_with_me
    }
    context = get_player_to_context(context, request)
    return render(request, template_name, context)


class GameDeleteView(generic.DeleteView):
    """
    class for deleting GoGame Object
    """
    model = GoGame
    template_name = 'forms/delete.html'
    context_object_name = 'game'
    success_url = reverse_lazy('organizer:go')


def trips(request):
    """
    Trips General View
    :param request:
    :return: renders a page
    """
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    template_name = 'trips/trips.html'
    context = {
        'trips': Trip.objects.all()
    }
    context = get_player_to_context(context, request)

    return render(request, template_name, context)


def new_trip(request):

    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'forms/default.html'
    success_url = reverse_lazy('organizer:trips')
    if request.method == 'POST':
        form = TripInitForm(request.POST)
        if form.is_valid():
            my_trip = Trip()
            my_trip.destination = form.cleaned_data['destination']
            my_trip.person1 = request.user
            if form.cleaned_data['person2']:
                my_trip.person2 = User.objects.get(pk=int(form.cleaned_data['person2']))
            if form.cleaned_data['person3']:
                my_trip.person3 = User.objects.get(pk=form.cleaned_data['person3'])
            if form.cleaned_data['person4']:
                my_trip.person4 = User.objects.get(pk=form.cleaned_data['person4'])
            my_trip.transport = form.cleaned_data['transport']
            my_trip.duration = form.cleaned_data['duration']
            my_trip.save()

            return HttpResponseRedirect(success_url)
    else:
        form = TripInitForm()
    context = {
        'form': form,
        'title': 'New Trip'
    }
    context = get_player_to_context(context, request)
    return render(request, template_name, context)


def trip(request, trip_id):

    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    m_trip = get_object_or_404(Trip, pk=trip_id)
    template_name = 'trips/trip.html'
    context = {
        'trip': m_trip
    }
    context = get_player_to_context(context, request)
    return render(request, template_name, context)


def trip_init(m_trip):
    output = {'destination': m_trip.destination}
    if m_trip.person2:
        output['person2'] = m_trip.person2
    if m_trip.person3:
        output['person3'] = m_trip.person3
    if m_trip.person4:
        output['person4'] = m_trip.person4
    if m_trip.start:
        output['start'] = m_trip.start
    output['duration'] = m_trip.duration
    if m_trip.transport:
        output['transport'] = m_trip.transport
    if m_trip.expected_distance:
        output['expected_distance'] = m_trip.expected_distance
    if m_trip.fuel_cost:
        output['fuel_cost'] = m_trip.fuel_cost
    if m_trip.plane_ticket_per_person:
        output['plane_ticket_per_person'] = m_trip.plane_ticket_per_person
    if m_trip.train_ticket_per_person:
        output['train_ticket_per_person'] = m_trip.train_ticket_per_person
    if m_trip.fuel_consumption:
        output['fuel_consumption'] = m_trip.fuel_consumption
    return output


def trip_edit(request, trip_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    m_trip = get_object_or_404(Trip, pk=trip_id)
    success_url = reverse('organizer:trip_display', kwargs={"trip_id": trip_id})
    template_name = 'trips/edit.html'
    if request.method == 'POST':
        if m_trip.transport == "car":
            form = TripEditFormCar(request.POST)
        elif m_trip.transport == 'bike':
            form = TripEditFormBike(request.POST)
        elif m_trip.transport == 'plane':
            form = TripEditFormPlane(request.POST)
        else:
            form = TripEditFormTrain(request.POST)
        if form.is_valid():
            m_trip.destination = form.cleaned_data['destination']
            m_trip.person1 = request.user

            if m_trip.transport == 'car':
                m_trip.expected_distance = form.cleaned_data['expected_distance']
                m_trip.fuel_cost = form.cleaned_data['fuel_cost']
                m_trip.fuel_consumption = form.cleaned_data['fuel_consumption']
            elif m_trip.transport == 'bike':
                m_trip.expected_distance = form.cleaned_data['expected_distance']
            elif m_trip.transport == 'plane':
                m_trip.plane_ticket_per_person = form.cleaned_data['plane_ticket_per_person']
            else:
                m_trip.train_ticket_per_person = form.cleaned_data['train_ticket_per_person']

            if form.cleaned_data['person2']:
                m_trip.person2 = User.objects.get(pk=int(form.cleaned_data['person2']))
            if form.cleaned_data['person3']:
                m_trip.person3 = User.objects.get(pk=form.cleaned_data['person3'])
            if form.cleaned_data['person4']:
                m_trip.person4 = User.objects.get(pk=form.cleaned_data['person4'])
            m_trip.transport = form.cleaned_data['transport']
            m_trip.duration = form.cleaned_data['duration']
            m_trip.start = form.cleaned_data['start']

            m_trip.save()
            m_trip.sum_up_cost()

            return HttpResponseRedirect(success_url)
    else:
        if m_trip.transport == "car":
            form = TripEditFormCar(initial=trip_init(m_trip))
        elif m_trip.transport == 'bike':
            form = TripEditFormBike(initial=trip_init(m_trip))
        elif m_trip.transport == 'plane':
            form = TripEditFormPlane(initial=trip_init(m_trip))
        else:
            form = TripEditFormTrain(initial=trip_init(m_trip))
    context = {
        'trip': m_trip,
        'form': form,
    }
    context = get_player_to_context(context, request)
    return render(request, template_name, context)


def trip_finances(request, trip_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    m_trip = get_object_or_404(Trip, pk=trip_id)
    template_name = 'trips/finances.html'
    context = {
        'trip': m_trip,
        'costs': TripCost.objects.filter(trip=m_trip)
    }
    if m_trip.transport == 'car' and m_trip.fuel_consumption and m_trip.expected_distance:
        context['car'] = True
        context['fuel'] = m_trip.fuel_cost * m_trip.fuel_consumption * m_trip.expected_distance / 100
    elif m_trip.transport == 'train' and m_trip.train_ticket_per_person:
        context['train'] = True
        context['ticket'] = m_trip.train_ticket_per_person * len(m_trip.members())
    elif m_trip.transport == 'plane' and m_trip.plane_ticket_per_person:
        context['plane'] = True
        context['ticket'] = m_trip.plane_ticket_per_person * len(m_trip.members())

    context = get_player_to_context(context, request)
    return render(request, template_name, context)


def new_cost(request, trip_id):

    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    m_trip = get_object_or_404(Trip, pk=trip_id)

    template_name = 'forms/default.html'
    success_url = reverse('organizer:trip_finances', kwargs={'trip_id': trip_id})
    if request.method == 'POST':
        form = TripCostForm(request.POST)
        if form.is_valid():
            cost = TripCost()
            cost.trip = m_trip
            cost.description = form.cleaned_data['description']
            cost.cost = form.cleaned_data['cost']
            cost.one_person_cost = form.cleaned_data['one_person_cost']
            cost.save()
            m_trip.save()
            m_trip.sum_up_cost()

            return HttpResponseRedirect(success_url)
    else:
        form = TripCostForm()
    context = {
        'title': f"New {m_trip} Cost",
        'form': form,
    }
    context = get_player_to_context(context, request)

    return render(request, template_name, context)

