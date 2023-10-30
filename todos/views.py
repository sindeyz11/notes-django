from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView
from django.db.models import Q

from .forms import TodoCreateForm, TodoUpdateForm
from .models import Todo


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todos/index.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('lastvisited') != 'todos':
            request.session['lastvisited'] = 'todos'

        # можно было сделать в запросе ниже, но так менее нагружено
        if request.GET.get('disablecompleted', False):
            if request.GET.get('disablecompleted', False) == 'false':
                request.session['filter'] = False
            else:
                request.session['filter'] = True

        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = dict()

        if self.request.GET.get('search', False):
            searchquery = self.request.GET['search']

            data['todo_list'] = Todo.objects.prefetch_related('tags').filter(
                Q(title__icontains=searchquery) | Q(description__icontains=searchquery),
                user=self.request.user,
            )
            data['searchquery'] = searchquery
        else:
            if self.request.session.get('filter', False):
                data['todo_list'] = Todo.objects.prefetch_related('tags').filter(
                    user=self.request.user,
                    is_completed=False
                )
                data['checked'] = 'checked'
            else:
                data['todo_list'] = Todo.objects.prefetch_related('tags').filter(user=self.request.user)

        return data


class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todos/todo_detail.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Todo.objects.prefetch_related('tags'), pk=self.kwargs['pk'])
        if self.request.user != obj.user:
            raise Http404

        return obj


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    template_name = 'todos/todo_update.html'
    # fields = ['title', 'description', 'tags', 'is_completed']
    form_class = TodoUpdateForm

    def get_object(self, queryset=None):
        obj = get_object_or_404(Todo, pk=self.kwargs['pk'])
        if self.request.user != obj.user:
            raise Http404

        return obj

    def form_valid(self, form):
        if form.instance.is_completed:
            form.instance.time_completed = timezone.now()

        return super(TodoUpdateView, self).form_valid(form)


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'todos/todo_create.html'
    # fields = ['title', 'description', 'tags']
    form_class = TodoCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TodoCreateView, self).form_valid(form)


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление без подтверждения
    """

    model = Todo
    success_url = reverse_lazy('todo-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.request.user != self.object.user:
            raise Http404
        self.object.delete()

        return redirect(self.get_success_url())


@login_required
def change_state(request, pk):
    obj = get_object_or_404(Todo, pk=pk)
    obj.is_completed = (not obj.is_completed)
    obj.time_completed = timezone.now()
    obj.save()
    return redirect(reverse_lazy('todo-list'))
