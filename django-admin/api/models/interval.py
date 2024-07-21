from django.db import models
import uuid
from .account import Account
from django.core.validators import MinValueValidator, MaxValueValidator

__all__ = [
    'Interval',
]


class Interval(models.Model):
    """
    Интервал для сообщений
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField(to=Account, on_delete=models.CASCADE, verbose_name='Аккаунт')
    interval = models.SmallIntegerField(
        verbose_name='Интервал в минутах',
        null=False,
        default=5,
        validators=[
            MaxValueValidator(60),
            MinValueValidator(1)]
    )

    def to_dict(self):
        return {
            'account': self.account.to_dict(),
            'interval': self.interval,
        }

    class Meta:
        verbose_name = 'Интервал'
        verbose_name_plural = 'Интервалы'
