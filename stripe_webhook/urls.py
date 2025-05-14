from django.urls import path
from .views import *

urlpatterns = [
    path('stripe/webhook/', stripe_webhook),
    path('stripe/obtener-datos/<str:session_id>/', obtener_datos_pago),
]