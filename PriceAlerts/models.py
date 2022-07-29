from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# status_choice = (("1" , "created"), ("2", "triggered"), ("3", "deleted"))

# Improvements : we can create different table for status and relate with Alerts so we can add more status if needed in future

# Model to save current active alerts of all users
class Alerts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.TextField(max_length=50)
    target_price = models.IntegerField()
    status = models.TextField(max_length = 20)
    created_on = models.DateTimeField(auto_now_add=True)


# Alerts Deleted, triggered will be saved as backup in this model so we can save time while running background task
class AllBackupAlerts(models.Model):
    alert = models.IntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.TextField(max_length=50)
    target_price = models.IntegerField()
    status = models.TextField(max_length = 20)
    created_on = models.DateTimeField(auto_now_add=True)
    # target_achieved_date = models.DateTimeField(auto_now_add=True)



