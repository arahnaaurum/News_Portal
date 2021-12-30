import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timedelta

from ...models import Author, Post, SubUser


logger = logging.getLogger(__name__)



def my_job():
    post_list = Post.objects.filter(time_creation__range=[datetime.now() - timedelta(days=7), datetime.now()])
    for subuser in SubUser.objects.all():
        post_list_category = post_list.filter(post_category = subuser.category)
        html_content = render_to_string(
            'weekly.html',
            {
                'post_list': post_list_category,
                'post_category': subuser.category,
                'username': subuser.sub_user.username,
            }
        )
        msg = EmailMultiAlternatives(
            subject='Weekly Update',
            body='',
            from_email='arahna.aurum@yandex.ru',
            to=[subuser.user_email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


# функция, которая будет очищать счетчик постов
def clean_max():
    for author in Author.objects.all():
        author.clean_maxpost()

# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # еженедельная рассылка писем
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'")

        # в полночь очищаются счетчики постов для авторов
        scheduler.add_job(
            clean_max,
            trigger=CronTrigger( hour="00"),
            id="clean_max",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
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