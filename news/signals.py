from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


@receiver(post_save, sender=Post)
def mailing(sender, instance, created, **kwargs):
    subscribers = instance.post_category.subscribers.all()
    for i in subscribers:
        if i.first_name:
            username = i.first_name
        else:
            username = i.username
        email = i.email
        if created:
            subject = f'Здравствуй, {username}. Новая новость: "{instance.headline}"'
        else:
            subject = f'Здравствуй, {username}. Новость "{instance.headline}" редактирована.'

        html_content = render_to_string(
            'news_created.html', {'post': instance}
        )

        msg = EmailMultiAlternatives(
            subject,
            body=instance.text,
            from_email='zhenyaradchikov@yandex.by',
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()
