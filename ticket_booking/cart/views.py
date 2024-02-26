from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .cart import Cart
from ticket_app.models import Event


# Create your views here.

def cart(request):
    cart = Cart(request)
    cart_events = cart.get_cart()
    num_tickets = cart.get_tickets()
    total = cart.get_total()
    context = {
        'cart_events': cart_events,
        'tickets': num_tickets,
        'total_price': total,

    }
    return render(request, 'cart.html', context=context)


def add_to_cart(request, event_id):
    cart = Cart(request)
    event_id = event_id

    regular_tickets = request.POST.get('select_regular') or None
    vip_tickets = request.POST.get('select_vip') or None

    if regular_tickets:
        event = get_object_or_404(Event, id=event_id)
        ticket_type = 'regular'
        ticket_price = event.regular_price
        tickets = regular_tickets
        data = {
            'event_id': event_id,
            'regular_tickets': tickets,
            'ticket_type': ticket_type,
            'price': ticket_price,
        }
    else:
        event = get_object_or_404(Event, id=event_id)
        ticket_type = 'VIP'
        ticket_price = event.vip_price
        tickets = vip_tickets

        data = {
            'event_id': event_id,
            'vip_tickets': tickets,
            'ticket_type': ticket_type,
            'price': ticket_price,
        }
    cart.add(event, tickets, ticket_type, ticket_price)
    return JsonResponse(data=data)


def delete_from_cart(request, event_id):
    cart = Cart(request)
    event = get_object_or_404(Event, id=event_id)

    # delete from cart session
    cart.delete(event=event_id)

    return redirect('cart')
