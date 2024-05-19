import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail
from .models import Post

logger = logging.getLogger(__name__)


def my_job(instance):
    fresh_articles = Post.objects.filter(date_published__gte=last_friday).order_by('title')[:3]

    if fresh_articles:
        articles_data = [{'title': article.title, 'url': article.get_absolute_url()} for article in fresh_articles]
        message = render_to_string('email/fresh_articles_email.html', {'articles': articles_data})

        for subscriber in instance.subscribers.all():
            send_mail(
                'Fresh Articles',
                message,
                'konstantin.eihman@yandex.ru',
                [subscriber.email],
                fail_silently=False,
            )
    else:
        logger.info("No fresh articles to send")


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="fri", hour="18"),
            id="my_job",  # The id assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job' to send fresh articles every Friday at 18:00.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions' to delete old job executions on Mondays.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
