from django.db import models
import uuid

__all__ = [
    'Message',
]


class Message(models.Model):
    """
    Сообщения в чатах
    """

    class MessageType(models.TextChoices):
        CHAT = 'CHAT', 'Чаты'
        PERSONAL = 'PERSONAL', 'Личные сообщения'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_type = models.CharField(
        verbose_name='Для каких чатов сообщения',
        max_length=16,
        choices=MessageType.choices,
        unique=True
    )
    message_text = models.TextField(verbose_name='Текст сообщения', null=False)

    def to_dict(self):
        return {
            'id': str(self.id),
            'message_type': self.message_type,
            'message_text': self.message_text,
        }

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
