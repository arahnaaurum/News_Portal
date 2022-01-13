import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

#периодические задачи по расписанию
app.conf.beat_schedule = {
    'action_send_posts_weekly': {
        'task': 'news_app.tasks.send_posts_weekly',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

app.autodiscover_tasks()