import random
import string

from django.db import models
from django.utils.http import urlsafe_base64_encode


class Secret(models.Model):

    generated_key = models.TextField(verbose_name="Ключ",
                                     null=True, blank=True)
    passphrase = models.CharField(max_length=100, verbose_name="Кодовое слово")
    secret = models.TextField(verbose_name="Секрет")
    time_to_live = models.IntegerField(default=43200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.generated_key} {self.passphrase} ' \
               f'{self.time_to_live}'

    class Meta:
        verbose_name = 'секрет'
        verbose_name_plural = 'секреты'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.generated_key = urlsafe_base64_encode(''.join(random.choices(
                string.ascii_uppercase + string.digits, k=25)).encode('utf-8'))
            self.passphrase = urlsafe_base64_encode(self.passphrase.encode('utf-8'))
        super().save(*args, **kwargs)
