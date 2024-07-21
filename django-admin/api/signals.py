from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from django.core.cache import caches
from json import loads, dumps


def ready():
    print('Signals is ready')


@receiver(post_save, sender=Account)
def save_account_to_redis(sender, instance, **kwargs):
    cache = caches['spammer']
    if instance.is_active:
        instance_dict = instance.to_dict()
        interval = Interval.objects.filter(account=instance).first()
        instance_dict['interval'] = interval.interval * 60 if interval else 5 * 60
        cache.set('active_account', dumps(instance_dict))

        chats = Chat.objects.filter(account=instance, is_active=True)
        cache.set('chat_list', dumps([chat.to_dict() for chat in chats]))
    else:
        cache.delete('active_account')
        cache.delete('chat_list')

    interval = Interval.objects.filter(account=instance).first()
    if not interval:
        interval = Interval.objects.create(
            account=instance
        )
        interval.save()


@receiver(post_save, sender=Message)
def save_message_to_redis(sender, instance, **kwargs):
    cache = caches['spammer']
    cache.set(f'messages:{instance.message_type.lower()}', dumps(instance.to_dict()))


@receiver(post_save, sender=Interval)
def save_interval_to_redis(sender, instance, **kwargs):
    cache = caches['spammer']
    active_account = cache.get('active_account', None)
    if not active_account:
        return

    active_account_data = loads(cache.get('active_account'))

    if active_account_data and active_account_data['id'] == instance.account.id:
        active_account_data['interval'] = instance.interval * 60

        cache.set('active_account', dumps(active_account_data))
