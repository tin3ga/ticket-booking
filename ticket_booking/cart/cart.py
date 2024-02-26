from ticket_app.models import Event


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')

        # If the user is new, no session key!  Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, event, tickets, ticket_type, ticket_price):
        event_id = str(event.id)
        tickets = str(tickets)
        ticket_price = str(ticket_price)

        # Logic

        self.cart[event_id] = {
            'tickets': int(tickets),
            'ticket_type': str(ticket_type),
            'ticket_price': float(ticket_price),
        }

        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_cart(self):
        # get id from session cart dict
        event_ids = self.cart.keys()

        # look up event in database by id
        events = Event.objects.filter(id__in=event_ids)

        return events

    def get_tickets(self):
        tickets = self.cart
        return tickets

    def get_total(self):
        # get id from session cart dict
        event_ids = self.cart.keys()

        # look up event in database by id
        events = Event.objects.filter(id__in=event_ids)

        # get tickets
        tickets = self.cart

        total = 0

        for key, value in tickets.items():
            for event in events:
                if event.id == int(key):
                    total = total + (value['tickets'] * value['ticket_price'])
        return total

    def delete(self, event):
        event_id = str(event)
        # Delete from cart if event id
        if event_id in self.cart:
            del self.cart[event_id]

        self.session.modified = True
