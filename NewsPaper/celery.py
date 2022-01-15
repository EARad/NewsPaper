import os
from celery import Celery
from celery.schedules import crontab



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'weekly_posts_monday_8am': {
        'task': 'weekly_posts',
        'schedule': crontab(),
    },
}
# minute='25', hour='21', day_of_week='Thu'