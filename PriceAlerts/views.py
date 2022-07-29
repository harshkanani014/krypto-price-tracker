from rest_framework.views import APIView
from rest_framework.response import Response
from Authentication.views import verify_token, get_error
from django.contrib.auth.models import User
import datetime
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from rest_framework import generics
from .models import Alerts, AllBackupAlerts
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .serializers import BackupAlertSerializer, UserAlertSerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
# Create your views here.


# Task : To create alert for currency and target price
# API endpoint : /create
# request : POST
class CreateAlert(APIView):
    def post(self, request):
        payload = verify_token(request)   
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        
        # Fetch requested data
        context = request.data
        context._mutable = True
        context['status'] = 'created'
        context['user'] = user.id
        context._mutable = False
        serializer = UserAlertSerializer(data=context)

        # verify data 
        if not serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(serializer.errors),
                "data": request.data
                })
    
        alert_save = serializer.save()
        
        alert_id = alert_save.id
        context._mutable = True
        context['alert'] = alert_id
        context._mutable = False

        # Save Data in BackupAlertsserializer so we retrieve data from fast and can some time while running background worker processes 
        backup_serializer = BackupAlertSerializer(data=context)
        if not backup_serializer.is_valid():
                return Response({
                "success":False,
                "message":get_error(backup_serializer.errors),
                "data": request.data
                })
        backup_serializer.save()
        
        # Set Interval Time in seconds so we can get more accuracy
        schedule, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS)
       
        # Add our schedule to periodic task and assign which task to perform
        task = PeriodicTask.objects.create(interval=schedule, name=str(alert_id), task='PriceAlerts.tasks.SendMailAlerts', start_time=datetime.datetime.now()+datetime.timedelta(seconds=20), last_run_at=datetime.datetime.now()-datetime.timedelta(seconds=10))
        return Response({
                "success":True,
                "message": "Your Alert Added successfully. You will be notified by email when currency will reach your target price",
                "data": request.data
                })


# Task : To create alert for currency and target price
# API endpoint : /delete
# request : DELETE
class DeleteAlert(APIView):
    def delete(self, request, id):
        # verify user
        payload = verify_token(request)   
        try:
            user = User.objects.filter(id=payload['id']).first()
        except:
            return payload
        
        # Delete current Alert
        alerts = Alerts.objects.get(id=id)
        alerts.delete()

        # change backup alert status to deleted
        backup_alert = AllBackupAlerts.objects.get(alert=id)
        backup_alert.status = "deleted"
        backup_alert.save()

        # Also Delete particular alert from Periodic Task so it scheduler will not assign this task to celery worker
        PeriodicTask.objects.filter(name=str(id)).delete()
        return Response({
            "success":True,
            "message":"Alert Deleted Successfully",
        })


# Standard Pagination class to set page limit
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


# Get all alerts with added cached layer so we can retrive data faster when we user to access them frequently.
# Request : GET
# API endpoint : /get-alerts
# Note : Filters and Pagination added
class GetAllAlerts(generics.ListAPIView):
    queryset = AllBackupAlerts.objects.all()
    serializer_class = BackupAlertSerializer
    filter_backends = [DjangoFilterBackend]

    # we can filter data with status, currenct and user
    filterset_fields = ['status', 'currency', 'user']
    pagination_class = StandardResultsSetPagination

    # Added default cache (Can be done using redis as well)
    @method_decorator(cache_page(60*60*2))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
   
  