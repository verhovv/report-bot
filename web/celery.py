import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

app = Celery('bot-template')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_max_loop_interval = 60
app.conf.beat_schedule = {
    'day-reminder': {
        'task': 'panel.tasks.remind',
        'schedule': crontab(minute='4,14,24,34,44,54'),
        'args': ('day',),
    },
    'evening-reminder': {
        'task': 'panel.tasks.remind',
        'schedule': crontab(minute='9,19,29,39,49,59'),
        'args': ('evening',),
    },
    'day-checker': {
        'task': 'panel.tasks.check_reports',
        'schedule': crontab(minute='5,15,25,35,45,55'),
        'args': ('day',),
    },
    'evening-checker': {
        'task': 'panel.tasks.check_reports',
        'schedule': crontab(minute='0,10,20,30,40,50'),
        'args': ('evening',),
    },
}