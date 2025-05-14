from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view
import stripe
import json
from django.conf import settings
stripe.api_key = 'sk_test_51ROTKbC0ISZZKwGbD573Oh5wcePqMB0VCyCo73LJhb2pS5kJ3c1iGB0j7bNum2RYUCTWSBOFiujiFXmzzBGKj8Jk00Dgk6Ue1k'
WEBHOOK_SECRET = 'whsec_mslWQRzRFrhNnFPh355UjaqqNqHSkPgI'

@api_view(['POST'])
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        print("✅ EVENTO:", event['type'])
    except stripe.error.SignatureVerificationError as e:
        print("❌ Firma inválida:", str(e))
        return HttpResponse(status=400)

    # Solo logueamos el pago, no guardamos nada
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print("🧾 PAGO CONFIRMADO PARA SESSION:", session['id'])

    return HttpResponse(status=200)

@api_view(['GET'])
def obtener_datos_pago(request, session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        metadata = session.get('metadata', {})
        return Response(metadata)
    except Exception as e:
        print("❌ ERROR:", str(e))
        return Response({'error': str(e)}, status=400)