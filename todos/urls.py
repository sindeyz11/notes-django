from django.urls import path

from . import views


urlpatterns = [
    path('', views.TodoListView.as_view(), name='todo-list'),
    path('<int:pk>/edit/', views.TodoUpdateView.as_view(), name='todo-update'),
    path('<int:pk>/', views.TodoDetailView.as_view(), name='todo-detail'),
    path('create/', views.TodoCreateView.as_view(), name='todo-create'),
    path('<int:pk>/delete/', views.TodoDeleteView.as_view(), name='todo-delete'),
    path('<int:pk>/change-state/', views.change_state, name='todo-change-state'),
]