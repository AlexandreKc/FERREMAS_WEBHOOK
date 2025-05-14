from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import stripe
import json
from django.http import JsonResponse
from django.conf import settings
stripe.api_key = 'sk_test_51ROTKbC0ISZZKwGbD573Oh5wcePqMB0VCyCo73LJhb2pS5kJ3c1iGB0j7bNum2RYUCTWSBOFiujiFXmzzBGKj8Jk00Dgk6Ue1k'
WEBHOOK_SECRET = 'whsec_mslWQRzRFrhNnFPh355UjaqqNqHSkPgI'

@csrf_exempt
@api_view(['POST'])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    print("\n🔥 WEBHOOK RECIBIDO")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    print(f"✅ EVENTO: {event['type']}")

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(f"✅ PAGO CONFIRMADO PARA SESSION: {session['id']}")
        return JsonResponse({"session_id": session['id'], "status": "PAGO"})

    return JsonResponse({"status": "NO PAGO"})


# DEBUG: obtener detalles de la sesión desde Stripe
@api_view(['GET'])
def obtener_datos_pago(request, session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return JsonResponse(session)
    except Exception as e:
        print(f"❌ ERROR AL OBTENER DATOS DE SESION: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)
