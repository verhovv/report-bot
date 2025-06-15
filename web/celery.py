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
        'schedule': crontab(hour='11', minute='55'),
        'args': ('day',),
    },
    'evening-reminder': {
        'task': 'panel.tasks.remind',
        'schedule': crontab(hour='20', minute='55'),
        'args': ('evening',),
    },
    'day-checker': {
        'task': 'panel.tasks.check_reports',
        'schedule': crontab(hour='12', minute='5'),
        'args': ('day',),
    },
    'evening-checker': {
        'task': 'panel.tasks.check_reports',
        'schedule': crontab(hour='21', minute='5'),
        'args': ('evening',),
    },
}
