from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages

# Create your views here.

def logout(request):
    request.session.flush()
    return redirect('/')

def index(request):
    if 'user_id' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    other_trips = Trip.objects.exclude(created_by=user)

    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "user_trips": user.trips.order_by('start_date'),
        "joined_trips": user.joined_trips.order_by('start_date'),
        "other_trips": other_trips.order_by('start_date')
    }

    return render(request, "index.html", context)

def new_trip(request):
    context = {
        "user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, "create.html", context)

def create(request):
    if request.method == "POST":
        errors = Trip.objects.trip_validator(request.POST)

        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/dashboard/newtrip')
        
        user=User.objects.get(id=request.session['user_id'])
        new_trip = Trip.objects.create(destination=request.POST['destination'], start_date=request.POST['start_date'],
        end_date=request.POST['end_date'],
        plan=request.POST['plan'],
        created_by = user)

    return redirect('/dashboard')


def view(request, id):
    this_trip = Trip.objects.get(id=id)

    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "this_trip" : this_trip,
        "all_joined_users": this_trip.joined_by.all(),
        "created_by": this_trip.created_by
    }

    return render(request, "view.html", context)

def edit(request, id):
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "this_trip" : Trip.objects.get(id=id)
    }

    return render(request, "edit.html", context)

def update(request, id):
    if request.method == "POST":

        errors = Trip.objects.trip_validator(request.POST)

        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect(f'/dashboard/{id}/edit')

        this_trip = Trip.objects.get(id=id)

        this_trip.destination = request.POST['destination']
        this_trip.start_date = request.POST['start_date']
        this_trip.end_date = request.POST['end_date']
        this_trip.plan = request.POST['plan']

        this_trip.save()

    return redirect('/dashboard')

def join(request, id):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        trip = Trip.objects.get(id=id)
        trip.joined_by.add(user)

    return redirect('/dashboard')

def cancel(request, id):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        trip = Trip.objects.get(id=id)
        trip.joined_by.remove(user)

    return redirect('/dashboard')

def remove(request, id):
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "this_trip": Trip.objects.get(id=id)
    }
    return render(request, "remove.html", context)

def destroy(request, id):
    if request.method=="POST":
        trip = Trip.objects.get(id=id)
        trip.delete()

    return redirect('/dashboard')