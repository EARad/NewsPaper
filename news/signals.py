from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .tasks import news_mail
# from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


''' Функция работает при помощи сигналов '''
# @receiver(post_save, sender=Post)
# def mailing(sender, instance, created, **kwargs):
#     subscribers = instance.post_category.subscribers.all()
#     for i in subscribers:
#         if i.first_name:
#             username = i.first_name
#         else:
#             username = i.username
#         email = i.email
#         if created:
#             subject = f'Здравствуй, {username}. Новая новость: "{instance.headline}"'
#         else:
#             subject = f'Здравствуй, {username}. Новость "{instance.headline}" редактирована.'
#
#         html_content = render_to_string(
#             'news_created.html', {'post': instance}
#         )
#
#         msg = EmailMultiAlternatives(
#             subject,
#             body=instance.text,
#             from_email='zhenyaradchikov@yandex.by',
#             to=[email],
#         )
#         msg.attach_alternative(html_content, "text/html")
#
#         msg.send()


@receiver(post_save, sender=Post)
def save_mail(sender, instance, created, **kwargs):
    subscribers = instance.post_category.subscribers.all()
    mail = []
    for i in subscribers:
        mail.append(i.email)

    new_headline = instance.headline
    body = instance.text
    from_mail = 'zhenyaradchikov@yandex.by'

    if created:
        subject = f'Здравствуйте. Новая новость: "{new_headline}"'
    else:
        subject = f'Здравствуйте. Новость "{new_headline}" редактирована.'

    html_content = render_to_string(
        'news_created.html', {'post': instance}
    )
    news_mail.delay(mail, body, subject, html_content, from_mail)
