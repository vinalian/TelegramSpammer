from django.db import models
import uuid

__all__ = [
    'Account',
]


class Account(models.Model):
    """
    Телеграм-аккаунты пользователей
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=15, unique=True)
    api_id = models.CharField(max_length=64, unique=True)
    api_hash = models.CharField(max_length=64, unique=True)
    session_string = models.TextField(null=True, blank=True)
    phone_code_hash = models.CharField(max_length=255, null=True, blank=True)
    last_auth = models.DateTimeField('Последняя авторизация', default=None, null=True, blank=False)
    created_date = models.DateTimeField('Дата добавления', auto_now=True)
    is_active = models.BooleanField(verbose_name='Аккаунт активен?', default=False)
    is_banned = models.BooleanField(verbose_name='Забанен ли аккаунт?', default=False)

    def save(self, *args, **kwargs):
        if self.is_active:
            # Установить is_active=False для всех других объектов
            Account.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def to_dict(self):
        # Преобразование объекта в словарь
        return {
            'id': str(self.id),
            'phone_number': self.phone_number,
            'api_id': self.api_id,
            'api_hash': self.api_hash,
            'session_string': self.session_string,
            'phone_code_hash': self.phone_code_hash,
            'name': self.name
        }

    def __str__(self):
        return f'{self.name} ({self.phone_number})'

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
