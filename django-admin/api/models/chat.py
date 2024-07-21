from django.db import models
import uuid
from .account import Account

__all__ = [
    'Chat',
]


class Chat(models.Model):
    """
    Телеграм-чаты
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name='Название чаты', max_length=64, null=False)
    chat_id = models.BigIntegerField(verbose_name='ID чата', null=False, blank=False)
    account = models.ForeignKey(to=Account, verbose_name='Аккаунт', on_delete=models.CASCADE, null=False, blank=False)
    last_message_send = models.DateTimeField('Последнее сообщение отправлено', default=None, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Активен', default=True)
    is_banned = models.BooleanField(verbose_name='Забанен ли аккаунт в этом чате', default=False)

    def to_dict(self):
        return {
            'title': self.title,
            'chat_id': self.chat_id,
            'account': str(self.account.id),
            'last_message_send': self.last_message_send.isoformat() if self.last_message_send else None,
            'is_active': self.is_active
        }

    class Meta:
        unique_together = ('chat_id', 'account')
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
