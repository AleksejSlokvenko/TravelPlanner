from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages 
import bcrypt
from django.db.models import Q
from datetime import date

# Create your views here.

def index(request):
	return render(request, "index.html")

def userRegConf(request):
	errors = User.objects.regValidator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/")
	else:
		password = request.POST['pw']
		hashedPw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

		newuser = User.objects.create(name = request.POST['name'], userName= request.POST['usname'], password = hashedPw)

		request.session['loggedInUserID'] = newuser.id

		message = {
			'confirmmessage': "You have successfully register"
		}
		for key, value in message.items():
			messages.error(request, value)
	return redirect("/")

def userLogInConf(request):
	errors = User.objects.logInValidator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/")
	else:
		user = User.objects.filter(userName = request.POST['usname'])
		user = user[0]
		request.session['loggedInUserID'] = user.id
	return redirect("/userWelcomePage")

def userWelcomePage(request):
	print(request.POST)
	if 'loggedInUserID' not in request.session:
		errors = { 
			'noLoggedInUser': "you must be logged in to view this page"
		}
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/")
	
	loggedinuser = User.objects.get(id = request.session['loggedInUserID'])
	context = {
		'loggedInUser': loggedinuser,
		'myTrips': Trip.objects.filter(Q(creator = loggedinuser) | Q(wisher = loggedinuser)),
		'otherTrips': Trip.objects.exclude(Q(creator = loggedinuser) | Q(wisher = loggedinuser))
	}
	return render(request, "userWelcomePage.html", context)

def logOut(request):
	request.session.clear()
	return redirect("/")

def createDestination(request):
	now = date.today()
	now = str(now)
	context = {
		'date': now
	}
	return render(request, "createTripPage.html", context)

def destinationValidation(request):
	now = date.today()
	
	errors = Trip.objects.destinationValidation(request.POST)
	
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/destination/create")

	loggedinuser = User.objects.get(id = request.session['loggedInUserID'])

	newDestination = Trip.objects.create(destination = request.POST['destination'], description = request.POST['description'], creator = loggedinuser, startdate = request.POST['stdate'], enddate = request.POST['endate'])

	return redirect("/userWelcomePage")

def addToMyTrip(request, tripId):
	trip = Trip.objects.get(id = tripId)
	user = User.objects.get(id = request.session['loggedInUserID'])
	user.planned_for.add(trip)
	return redirect("/userWelcomePage")

def myDestinations(request, tripId):
	trip = Trip.objects.get(id = tripId)
	loggedinuser = User.objects.get(id = request.session['loggedInUserID'])
	context = {
		'trip': trip,
		'user': loggedinuser,
		'otherusers': Trip.objects.exclude(Q(creator = loggedinuser) | Q(wisher = loggedinuser)),
	}
	return render(request, "myDestinations.html", context)