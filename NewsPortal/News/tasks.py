from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import datetime
import time

from NewsPortal import settings
from News.models import Post, Category


@shared_task
def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    for subscriber in subscribers:
        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def send_last_week_news():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_time_in__gte=last_week)
    categories = set(posts.values_list('post_category__category_name', flat=True))
    subscribers_email = set(Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))

    for subscriber_email in subscribers_email:
        msg = EmailMultiAlternatives(
            subject='Статьи за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber_email],
        )
        html_content = render_to_string(
            'daily_post.html',
            {
                'link': settings.SITE_URL,
                'posts': set(posts.filter(post_category__subscribers__email=subscriber_email))
            }
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
