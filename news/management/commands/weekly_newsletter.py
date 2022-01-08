import logging

from django.conf import settings
# from decouple import config
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


# функция, которая будет выполняться
def my_job():
    for subscriber in User.objects.all():
        msg = []
        categories = subscriber.category_set.all()
        for category in categories:
            category_posts = []
            posts = category.post_set.all()
            for post in posts:
                if post.date.date() > datetime.now().date() - timedelta(days=7):
                    category_posts.append(f'{post.headline}: http://127.0.0.1:8000{post.get_absolute_url()}')
            msg.append(f'В вашей любимой категории "{category.category}" за прошедшую'
                       f' неделю появились посты: {category_posts}')
        message = '\n'.join(msg)
        print(message)


        send_mail(
            subject=f'Привет, {subscriber.username}.',
            message=message,
            from_email='zhenyaradchikov@yandex.by',
            recipient_list=[subscriber.email],
        )
        # config('EMAIL_HOST_USER')


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                day_of_week="Sat", hour="21", minute="28"
            ),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не
            # надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
