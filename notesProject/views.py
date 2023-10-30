from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render, resolve_url


def redirection_view(request):
    """
    Для редиректа
    """
    if request.session.get('lastvisited', False) == 'notes':
        return redirect('note-list')
    else:
        return redirect('todo-list')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        nxt = request.GET.get('next', False)

        if form.is_valid():
            user = form.save()
            login(request, user)

            if nxt:
                return redirect(resolve_url(nxt))

            return redirect("redirecturl")

        return render(request, 'registration/signup.html', {'form': form, 'next': nxt})

    form = UserCreationForm()
    nxt = request.GET.get('next', False)
    context = {
        'form': form,
        'next': nxt,
    }

    return render(request, 'registration/signup.html', context=context)