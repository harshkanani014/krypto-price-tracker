from django.contrib.auth.models import User
from celery import shared_task
from .models import *
import json
from django_celery_beat.models import PeriodicTask
import requests
from django.core.mail import EmailMultiAlternatives


# Function to send email
def send_email(email_1, currency, target_price):
    
    email = EmailMultiAlternatives("Krypto Alert!! Target Achieved on your alert of " + str(currency) , "Your " + str(target_price) + " of " + str(currency) + " achieved now. Please login into trading app for trading")
    email.to = [email_1]
    email.send()


# Schedule Task to send alert mail
@shared_task(bind=True)
def SendMailAlerts(self):
    all_alerts = Alerts.objects.all()
    current_price = 10000
    for alert in all_alerts:
        current_currency = alert.currency 
        response_API = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=" + current_currency + "&vs_currencies=USD")
        data = response_API.text
        data = json.loads(data)
        acurrent_price = data[current_currency]["usd"]
        print("price", acurrent_price)
        current_price = 10000
        if alert.target_price==int(current_price):
            user_data = User.objects.get(id=alert.user.id)
            send_email(user_data.email, current_currency, current_price)
            print("send mail")
            new_record = AllBackupAlerts.objects.get(alert=alert.id)
            new_record.status = "triggered"
            # new_record = AllBackupAlerts(user=alert.user, currency=alert.currency, target_price=alert.target_price, status="triggered", created_on=alert.created_on)
            new_record.save()
            PeriodicTask.objects.filter(name=str(alert.id)).delete()
            Alerts.objects.filter(id=alert.id).delete()
    return "Done"
