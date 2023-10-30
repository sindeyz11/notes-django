from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


from .models import Notification


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ('title', 'description', 'scheduled_for')

    def clean_scheduled_for(self):
        data = self.cleaned_data['scheduled_for']

        if data < timezone.now():
            raise ValidationError('Дата и время должны быть в будущем!')

        return data
