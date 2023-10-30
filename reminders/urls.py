from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='reminders-index'),
    path('create/', views.create_notification, name='reminder-create'),
    path('pending/', views.PendingRemindersListView.as_view(), name='reminder-pending'),
    path('clear/', views.clear_reminders, name='reminders-clear'),
    path('<int:pk>/', views.NotificationUpdateView.as_view(), name='reminder-update'),
]