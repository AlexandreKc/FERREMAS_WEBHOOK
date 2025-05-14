from django.urls import path
from .views import *

urlpatterns = [
    path('stripe/webhook/', stripe_webhook),
]