from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime

from .models import Post, PostCategory, Category, SubUser
from django.contrib.auth.models import User

@receiver(m2m_changed, sender = Post.post_category.through)
def new_post_notify(sender, instance, **kwargs):
    for subuser in SubUser.objects.all():
        if subuser.category in instance.post_category.all():
            html_content = render_to_string(
                'notification.html',
                {
                    'instance': instance,
                    'post_category': subuser.category,
                    'username': subuser.sub_user.username,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'{instance.title}',
                body=f'{instance.text}',
                from_email='arahna.aurum@yandex.ru',
                to=[f'{subuser.user_email}'],
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()

@receiver(post_save, sender=Post)
def update_counter(sender, instance, **kwargs):
    instance.author.update_maxpost()