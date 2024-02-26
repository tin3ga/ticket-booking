from django.shortcuts import render, get_object_or_404

from .models import Event


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
