from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('userRegConf', views.userRegConf),
    path('userWelcomePage', views.userWelcomePage),
    path('userLogInConf', views.userLogInConf),
    path('logOut', views.logOut),
    path('destination/create', views.createDestination),
    path('destinationValidation', views.destinationValidation),
    path('myDestinations/<tripId>', views.myDestinations),
    path("addToMyTrip/<tripId>", views.addToMyTrip),
    # path("removeWishFromList/<wishId>", views.removeWishFromList),
    # path("deleteWish/<wishId>", views.deleteWish)
]