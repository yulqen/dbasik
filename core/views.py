from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def index(request):
    return render(request, 'core/index.html')


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html', {'section': 'dashboard'})


def profile(request):
    args = {'user': request.user}
    return render(request, 'core/profile.html', args)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
        else:
            if form.errors:
                k_lst = list(form.errors.keys())[0]
                messages.add_message(request, messages.WARNING, form.errors[k_lst])
    else:
        form = UserCreationForm()

    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)
