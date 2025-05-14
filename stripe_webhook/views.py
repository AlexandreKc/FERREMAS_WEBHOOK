from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import stripe
import json
from django.conf import settings
stripe.api_key = 'sk_test_51ROTKbC0ISZZKwGbD573Oh5wcePqMB0VCyCo73LJhb2pS5kJ3c1iGB0j7bNum2RYUCTWSBOFiujiFXmzzBGKj8Jk00Dgk6Ue1k'
WEBHOOK_SECRET = 'whsec_mslWQRzRFrhNnFPh355UjaqqNqHSkPgI'

@csrf_exempt
@api_view(['POST'])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        print("❌ Firma inválida o payload corrupto:", e)
        return Response({"status": "NO PAGO"}, status=400)

    print(f"🔥 WEBHOOK RECIBIDO: {event['type']}")

    if event['type'] == 'checkout.session.completed':
        print("✅ PAGO")
        return Response({"status": "PAGO"}, status=200)
    else:
        print("❌ NO PAGO")
        return Response({"status": "NO PAGO"}, status=200)