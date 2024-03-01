from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .cart import Cart
from ticket_app.models import Event
from checkout.models import Ticket


# Create your views here.
@login_required(login_url='/login/')
def cart(request):
    cart = Cart(request)
    cart_events = cart.get_cart()
    num_tickets = cart.get_tickets()
    total = cart.get_total()

    price_ids = []
    for item in cart_events:
        for k, v in num_tickets.items():
            if k == str(item.id):
                details = {
                    "price": v['price_id'],
                    "quantity": v['tickets']
                }
        price_ids.append(details)


    context = {
        'cart_events': cart_events,
        'tickets': num_tickets,
        'total_price': total,
        'price_ids': price_ids,

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
        price_id = event.regular_stripe_id
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
        price_id = event.vip_stripe_id

        data = {
            'event_id': event_id,
            'vip_tickets': tickets,
            'ticket_type': ticket_type,
            'price': ticket_price,
        }

    tickets_qs = Ticket.objects.filter(order__user=request.user.id, event_name=event)

    num_reserved_tickets = int(tickets)
    for t in tickets_qs:
        num_reserved_tickets += t.tickets
    if num_reserved_tickets <= 5:
        cart.add(event, tickets, ticket_type, ticket_price, price_id)
        messages.success(request, f'{event.name} Tickets Successfully Added To Cart')
    else:
        messages.success(request,
                         f'Maximum number of individual tickets is 5. You have {num_reserved_tickets} reserved for this event')

    return redirect('cart')


def delete_from_cart(request, event_id):
    cart = Cart(request)
    event = get_object_or_404(Event, id=event_id)

    # delete from cart session
    cart.delete(event=event_id)
    messages.error(request, f'{event.name} Tickets Removed From Cart')
    return redirect('cart')
