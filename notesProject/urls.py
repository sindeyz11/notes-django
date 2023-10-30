"""
URL configuration for notesProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .views import redirection_view, signup


urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),

    path('', redirection_view, name='redirecturl'),  # idk is this allowed 0_o
    path('admin/', admin.site.urls),
    path('logoutlogin/', auth_views.logout_then_login, name='logoutlogin'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    path('todos/', include('todos.urls'), name='todos'),
    path('notes/', include('notes.urls'), name='notes'),
    path('reminders/', include('reminders.urls'), name='reminders'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)