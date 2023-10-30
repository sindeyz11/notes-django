from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, ListView

from .forms import NotificationForm
from .models import Notification


@login_required
def index(request):
    reminders = Notification.objects.filter(user=request.user, status=True)
    context = {
        'reminders': reminders
    }
    return render(request, 'reminders/index.html', context=context)


@login_required
def create_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user

            # TODO зарефакторить notification -> reminder
            # TODO меседж брокер

            form.save()
            return HttpResponseRedirect(reverse('reminders-index'))

        return render(request, 'reminders/reminder_create.html', {'form': form})

    else:
        default_scheduled = datetime.now() + timedelta(minutes=1)
        form = NotificationForm(initial={'scheduled_for': default_scheduled})
        context = {
            'form': form,
        }
        return render(request, 'reminders/reminder_create.html', context=context)


class NotificationUpdateView(LoginRequiredMixin, UpdateView):
    model = Notification
    template_name = 'reminders/reminder_update.html'
    # fields = ['title', 'description', 'scheduled_for']
    form_class = NotificationForm
    success_url = reverse_lazy('reminders-index')

    def get_object(self, queryset=None):
        obj = get_object_or_404(Notification, pk=self.kwargs['pk'])
        if self.request.user != obj.user:
            raise Http404

        return obj


@login_required
def clear_reminders(request):
    Notification.objects.filter(user=request.user, status=True).delete()
    return redirect(reverse_lazy('reminders-index'))


class PendingRemindersListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'reminders/pending_list.html'

    def get_queryset(self):
        now = datetime.now()
        return Notification.objects.filter(user=self.request.user, scheduled_for__gte=now)
