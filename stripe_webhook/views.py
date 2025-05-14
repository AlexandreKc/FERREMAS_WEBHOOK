from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view
import stripe
import json

stripe.api_key = 'sk_test_51ROTKbC0ISZZKwGbD573Oh5wcePqMB0VCyCo73LJhb2pS5kJ3c1iGB0j7bNum2RYUCTWSBOFiujiFXmzzBGKj8Jk00Dgk6Ue1k'
WEBHOOK_SECRET = 'whsec_mslWQRzRFrhNnFPh355UjaqqNqHSkPgI'

@csrf_exempt
@api_view(['POST'])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print("✅ Pago exitoso:", session.get('metadata', {}))

    return HttpResponse(status=200)