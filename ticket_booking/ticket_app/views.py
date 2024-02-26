from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from .models import Event
from .forms import RegisterUserForm, LoginForm


# Create your views here.

def home(request):
    events = Event.objects.all()
    context = {
        'events': events

    }
    return render(request, 'index.html', context=context)


def event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    context = {
        'event': event,
    }
    return render(request, 'event.html', context=context)


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = RegisterUserForm()

    return render(request, 'registration/sign_up.html', {"form": form})


# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})
