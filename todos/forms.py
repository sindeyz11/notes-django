from django import forms
from django.core.exceptions import ValidationError

from .models import Todo, Tag


class TodoAdminForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'user', 'tags']

    def clean(self):
        tags = self.cleaned_data.get('tags')
        if tags and tags.count() > 3:
            raise ValidationError('Нельзя выбрать больше 3 категорий')

        return self.cleaned_data


class TodoCreateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'tags']

    def clean(self):
        tags = self.cleaned_data.get('tags')
        if tags and tags.count() > 3:
            raise ValidationError('Нельзя выбрать больше 3 категорий')

        return self.cleaned_data


class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'tags', 'is_completed']

    def clean(self):
        tags = self.cleaned_data.get('tags')
        if tags and tags.count() > 3:
            raise ValidationError('Нельзя выбрать больше 3 категорий')

        return self.cleaned_data