from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User


@shared_task
def news_mail(mail, body, subject, html_content, from_mail):
    msg = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=from_mail,
        to=mail,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def weekly_posts():
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

        send_mail(
            subject=f'Привет, {subscriber.username}.',
            message=message,
            from_email='zhenyaradchikov@yandex.by',
            recipient_list=[subscriber.email],
        )
