from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


from .models import Post

@receiver(m2m_changed, sender=Post.subscribers.through)
def notify_subscribers(sender, instance, action, model, **kwargs):
    if action == 'post_add':
        subject = f'Новая новость: {instance.title}'
        text_content = f'Прочитайте новость "{instance.title}" на нашем сайте: http://127.0.0.1:8000/{instance.get_absolute_url()}'
        html_content = f'Прочитайте новость "{instance.title}" на нашем сайте: <a href="http://127.0.0.1:8000/{instance.get_absolute_url()}">Ссылка</a>'

        for subscriber in instance.subscribers.all():
            msg = EmailMultiAlternatives(subject, text_content, None, [subscriber.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()