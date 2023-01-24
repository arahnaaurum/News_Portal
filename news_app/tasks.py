from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timedelta

from .models import Author, Post, SubUser

# отправка списка постов каждую неделю - см. раписание в celery.py
@shared_task
def send_posts_weekly():
    post_list = Post.objects.filter(time_creation__range=[datetime.now() - timedelta(days=7), datetime.now()])
    for subuser in SubUser.objects.all():
        post_list_category = post_list.filter(post_category = subuser.category)
        html_content = render_to_string(
            'daily.html',
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

# отправка постов после создания без использования signals - см. views.py, в NewsCreateView переопределен метод post()
@shared_task
def send_new_post(newpost):
    for subuser in SubUser.objects.all():
        if subuser.category == newpost['post_category']:
            html_content = render_to_string(
                'notification.html',
                {
                    'instance': newpost['text'],
                    'post_category': subuser.category,
                    'username': subuser.sub_user.username,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'{newpost["title"]}',
                body=f'{newpost["text"]}',
                from_email='arahna.aurum@yandex.ru',
                to=[f'{subuser.user_email}'],
            )
            msg.attach_alternative(html_content, "text/html")

            msg.send()
