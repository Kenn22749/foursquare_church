from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Event, EventRegistration
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def event_list(request):
    # Show only active events, ordered by date
    events_list = Event.objects.filter(is_active=True).order_by('date')

    paginator = Paginator(events_list, 3)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)

    return render(request, 'events/list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/detail.html', {'event': event})


@login_required
def register_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if EventRegistration.objects.filter(event=event, member=request.user).exists():
        messages.info(request, "You already registered.")
    else:
        EventRegistration.objects.create(event=event, member=request.user)
        messages.success(request, "Registered for event.")
    return redirect('events-detail', pk=pk)


@login_required
def my_registrations(request):
    regs = EventRegistration.objects.filter(member=request.user).select_related('event')
    return render(request, 'events/my_registrations.html', {'regs': regs})
