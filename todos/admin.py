from django.contrib import admin

from .models import Todo, Tag
from .forms import TodoAdminForm


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    form = TodoAdminForm


admin.site.register(Tag)