import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insure.settings')

app = Celery('insure')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     'task_name': {
#         'task': 'main_app.tasks.my_task',
#         'schedule': crontab(),
#     }
# }


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request}')
