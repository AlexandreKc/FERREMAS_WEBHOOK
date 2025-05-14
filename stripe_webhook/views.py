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
    print("🔥 WEBHOOK RECIBIDO")

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        print("✅ FIRMA VÁLIDA - Evento:", event['type'])
    except stripe.error.SignatureVerificationError as e:
        print("❌ FIRMA INVÁLIDA:", str(e))
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get('metadata', {})
        print("🧾 METADATA:", metadata)

        try:
            pedido = Pedido.objects.create(
                usuario_id=metadata['usuario'],
                total=metadata['total'],
                estado='ACEPTADO',
                tipo_despacho_id=metadata['tipo_despacho_id'],
                direc_desp=metadata.get('direc_desp') or None,
                id_comuna_dep=metadata.get('id_comuna_dep') or None,
                id_region_desp=metadata.get('id_region_desp') or None,
                tipo_comprobante_id=metadata['tipo_comprobante_id'],
                rut_factura=metadata.get('rut_factura') or None,
                razon_social=metadata.get('razon_social') or None,
                id_sucursal=metadata.get('id_sucursal') or None,
                stripe_session_id=session['id']
            )
            print("✅ PEDIDO GUARDADO:", pedido.id)
        except Exception as e:
            print("❌ ERROR AL CREAR PEDIDO:", str(e))
            return HttpResponse(status=500)

    return HttpResponse(status=200)