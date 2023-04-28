from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from News.models import PostCategory
from News.tasks import send_notifications


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.post_category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications.delay(instance.preview(), instance.pk, instance.post_title, subscribers)
