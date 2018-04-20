from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages


def index(request):
    return render(request, 'core/index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
        else:
            if form.errors:
                k_lst = list(form.errors.keys())[0]
                messages.add_message(request, messages.WARNING, form.errors[k_lst])
    else:
        form = UserCreationForm()

    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)
