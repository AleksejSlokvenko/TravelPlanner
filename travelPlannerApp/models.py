from django.db import models
import bcrypt
import re
import datetime


# Create your models here.
class ValidationManager(models.Manager):
    def regValidator(self, postData):
        errors = {}
       
        if len(postData['name']) < 1:
            errors["name"] = "Name is required"
       
        if len(postData['usname']) < 1:
            errors["usname"] = "User name Name is required"
        usersWithUserName = User.objects.filter(userName = postData['usname'])
        if len(usersWithUserName) > 0:
            errors ['ustaken'] = "This username is already taken, please you another username"
       
        if len(postData['pw']) < 1:
            errors["pw"] = "Passwrord is required"
        if len(postData['pw']) < 8:
            errors["pwlength"] = "Passwrord has to be atleast 8 charactres long"
        if postData['pw'] != postData['cpw']:
            errors["pwconfirm"] =  "Password has to match"
        
        
        return errors

    def logInValidator(self, postData):
        errors = {}
        if len(postData['usname']) < 1:
            errors ['usnamemissing'] = "Please enter your Username"
        usersWithUserName = User.objects.filter(userName = postData['usname'])
        if len(usersWithUserName) == 0:
            errors ['usnametaken'] = "No username, plaese register first"
        else:
            user = usersWithUserName[0]
            if bcrypt.checkpw(postData['pw'].encode(), user.password.encode()):
                print("Password match")
            else:
                print("Failed password")
                errors ['incorectpw'] = "Invalid password"
        
        return errors 
    
    def destinationValidation(self, postDATA):
        time = datetime.datetime.now()
        now = time.strftime("%Y-%m-%d")
        errors = {}

        if len(postDATA['destination']) < 1:
            errors ['destMissing'] = "Please enter a destination"
            print(errors)

        if len(postDATA['description']) < 5:
            errors["description"] =  "Description needs be more than 5 character"
            print(errors)

        if len(postDATA["stdate"])< 1:
            errors["startdate"] = "Date is required"
            print(errors)
        if len(postDATA["endate"])< 1:
            errors["enddate"] = "Trip end date is Required"
            print(errors)
        if postDATA["stdate"] > postDATA['endate']:
            errors["stardate"]="Start date cannot be past end date"
            print(errors)
        if postDATA["stdate"] < now:
            errors["stdate"]="Please don't enter a date in the past"
            print(errors)
        return errors


class User(models.Model):
    name = models.CharField(max_length = 45)
    userName = models.CharField(max_length = 45)
    password = models.CharField(max_length = 45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ValidationManager()

class Trip(models.Model):
    destination = models.CharField(max_length = 45)
    description = models.TextField()
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    creator = models.ForeignKey(User, related_name="trip_created", on_delete= models.CASCADE)
    wisher = models.ManyToManyField(User, related_name="planned_for")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ValidationManager()