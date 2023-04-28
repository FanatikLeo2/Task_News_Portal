import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_last_week_news_every_monday_8am': {
        'task': 'News.tasks.send_last_week_news',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
