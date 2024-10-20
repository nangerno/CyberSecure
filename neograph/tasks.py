# tasks.py
from celery import shared_task
from .models import MitreServer

@shared_task
def my_task():
    # This is a test task
    print("Test task executed successfully!")

@shared_task
def update_mitre(pk):
    print('Updating MITRE data')
    server = MitreServer.objects.get(id=pk)
    server.update_data()
    print('Done Updating MITRE data')
