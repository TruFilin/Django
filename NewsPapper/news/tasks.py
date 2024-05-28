from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Post, Subscriber
from datetime import timedelta


@shared_task
def send_notification_to_subscribers(news_id):
    news = Post.objects.get(id=news_id)
    subscribers = Subscriber.objects.all()

    for subscriber in subscribers:
        send_mail(
            'Новая новость',
            f'Заголовок: {news.title}\nТекст: {news.content}',
            'from@example.com',
            [subscriber.email],
            fail_silently=False,
        )


@shared_task
def send_weekly_newsletter():
    last_week = timezone.now() - timedelta(days=7)
    latest_news = Post.objects.filter(date_created__gte=last_week)

    for subscriber in Subscriber.objects.all():
        news_content = '\n'.join([f'{news.title}: {news.content}' for news in latest_news])
        send_mail(
            'Еженедельный дайджест новостей',
            news_content,
            'from@example.com',
            [subscriber.email],
            fail_silently=False,
        )
