from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView

from .forms import NoteForm
from .models import Note


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/index.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('lastvisited') != 'notes':
            request.session['lastvisited'] = 'notes'

        return super().get(self, request, *args, **kwargs)

    # paginate_by = 4
    def get_context_data(self, **kwargs):
        notes = Note.objects.filter(user=self.request.user)

        paginator = Paginator(notes, 4)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        data = {'notes': notes, 'page_obj': page_obj}
        return data


@login_required
def note_update(request, slug):
    note = get_object_or_404(Note, slug=slug)

    if note.user != request.user:
        return Http404

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('note-list'))
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes/note_update.html', {'form': form})


@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return HttpResponseRedirect(reverse_lazy('note-list'))

    else:
        form = NoteForm()

    return render(request, 'notes/note_create.html', {'form': form})
