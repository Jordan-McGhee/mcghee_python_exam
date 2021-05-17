from django.db import models
from login_registration_app.models import *

# Create your models here.
class TripManager(models.Manager):
    def trip_validator(self, postData):
        todays_date = datetime.now().date()
        date_format = "%Y-%m-%d"

        # if postData['start_date'] and postData['end_data']:
        #     start_input = datetime.strptime(postData['start_date'], date_format).date()
        # if postData['end_date']:
        #     end_input = datetime.strptime(postData['end_date'], date_format).date()

        errors = {}

        # Making sure destination/plan > 3 and date fields aren't empty

        if len(postData['destination']) < 3:
            errors['destination'] = "Destination must be at least 3 characters"

        if len(postData['plan']) < 3:
            errors['plan'] = "Plan must be at least 3 characters"

        if not postData['start_date']:
            errors['start_date'] = "Please enter a start date"

        if not postData['end_date']:
            errors['end_date'] = "Please enter an end date"

        if postData['start_date'] and postData['end_date']:
            start_input = datetime.strptime(postData['start_date'], date_format).date()
            end_input = datetime.strptime(postData['end_date'], date_format).date()

            if todays_date > start_input:
                errors['start_date'] = "Please select a start date in the future"

            if start_input > end_input:
                errors['end_date'] = "Unless you're going to teach me how to time travel on this trip, please select an end date that's after your start date"

        return errors

        

class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    created_by = models.ForeignKey(User, related_name = "trips", on_delete = models.CASCADE)
    joined_by = models.ManyToManyField(User, related_name = "joined_trips")
    objects = TripManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)