from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.urls import reverse_lazy


class Todo(models.Model):
    title = models.CharField('Название', max_length=32)
    description = models.TextField('Описание', blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", blank=True, verbose_name='Категории')
    is_completed = models.BooleanField('Выполнено?', default=False)
    time_created = models.DateTimeField(auto_now_add=True)
    time_completed = models.DateTimeField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse_lazy('todo-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['is_completed', '-last_modified']


class Tag(models.Model):
    title = models.CharField(max_length=16)

    def __str__(self):
        return self.title
