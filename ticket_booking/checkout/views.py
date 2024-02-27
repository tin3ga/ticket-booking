import time
import stripe
import json

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


# Create your views here.
def stripe_checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    if request.method == 'POST':
        price_ids = request.POST.get('price_ids')
        print(price_ids)
        data = json.loads(price_ids.replace("'", '"'))
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=data,
            mode='payment',
            customer_creation='always',
            success_url=settings.REDIRECT_DOMAIN + '/checkout/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.REDIRECT_DOMAIN + '/checkout/payment_cancelled',
        )
        return redirect(checkout_session.url, code=303)


## use Stripe dummy card: 4242 4242 4242 4242
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    amount_total = session["amount_total"]
    customer_email = session["customer_details"]["email"]
    payment_status = session["payment_status"]
    payment_intent = session["payment_intent"]
    customer = stripe.Customer.retrieve(session.customer)

    return render(request, 'payment_successful.html', {'customer': customer})


def payment_cancelled(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    return render(request, 'payment_cancelled.html')


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        print('got here')
        return redirect('payment_successful')
    return HttpResponse(status=200)
