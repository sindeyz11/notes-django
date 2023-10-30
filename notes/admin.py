from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    # fields = ['title', 'main_text', 'user']

    # Чтобы сделать slug необязательным параметром в админке
    def get_form(self, request, obj=None, **kwargs):
        form = super(NoteAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['slug'].required = False
        return form
