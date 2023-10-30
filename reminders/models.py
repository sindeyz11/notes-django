from django.conf import settings
from django.db import models


class Notification(models.Model):
    title = models.CharField('Название', max_length=16)
    description = models.CharField('Описание', max_length=128, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    scheduled_for = models.DateTimeField('Запланировать на')
    status = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
