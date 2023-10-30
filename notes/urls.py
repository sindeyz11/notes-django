from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.NoteListView.as_view(), name='note-list'),
    path('create/', views.note_create, name='note-create'),
    path('<slug:slug>/', views.note_update, name='note-detail'),
]