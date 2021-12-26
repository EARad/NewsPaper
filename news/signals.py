from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Category, PostCategory
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


@receiver(post_save, sender=Post)
def mailing(sender, instance, created, **kwargs):

    y = instance.category_post_set.all()
    print(y)

    # subscribers = Category.objects.get(category=y).subscribers.all()
    # print(subscribers)

    # for i in subscribers:
    #     email = i.email
    #     if created:
    #         subject = f'Новая новость: {instance.headline}'
    #     else:
    #         subject = f'Новость {instance.headline} редактирована.'
    #
    #     html_content = render_to_string(
    #         'news_created.html', {'post': instance}
    #     )
    #
    #     msg = EmailMultiAlternatives(
    #         subject,
    #         body=instance.text,
    #         from_email='zhenyaradchikov@yandex.by',
    #         to=[email],
    #     )
    #     msg.attach_alternative(html_content, "text/html")
    #
    #     msg.send()
