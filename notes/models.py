from django.conf import settings
from django.db import models

from .utils import slugify


class Note(models.Model):
    title = models.CharField('Заголовок', max_length=255, blank=True, help_text='Опционально')
    main_text = models.TextField(verbose_name='Текст заметки')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)
    time_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title if self.title else self.main_text[:8] + '..'

    # -_-
    def get_slug(self):
        slug = slugify(str(self))
        unique_slug = slug

        number = 1
        while Note.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{number}'
            number += 1

        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_slug()
        return super(Note, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-last_modified']
