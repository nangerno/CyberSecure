from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_proj.settings')

app = Celery('dj_proj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'my-test-task': {
        'task': 'neograph.tasks.my_task',
        'schedule': 20,  # Example: run the task every 20 seconds
    },
    'update_mitre': {
        'task': 'neograph.tasks.update_mitre',  
        'schedule': crontab(minute=0, hour=0),  # Run the task every day at midnight 
        'args': (3,),  
    },
    
}

app.conf.timezone = 'UTC'
