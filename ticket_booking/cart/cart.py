class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')

        # If the user is new, no session key!  Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, event, tickets, ticket_type):
        event_id = str(event.id)
        tickets = str(tickets)

        # Logic

        self.cart[event_id] = {
            'tickets': int(tickets),
            'ticket_type': str(ticket_type)
        }

        self.session.modified = True

    def __len__(self):
        return len(self.cart)