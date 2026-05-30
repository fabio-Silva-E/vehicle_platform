import json

from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Payment


@csrf_exempt
def asaas_webhook(request):

    # aceita apenas POST
    if request.method != "POST":

        return JsonResponse({"error": "Método inválido"}, status=405)

    # valida token
    token = request.headers.get("asaas-access-token")

    if token != settings.ASAAS_WEBHOOK_TOKEN:

        return JsonResponse({"error": "Token inválido"}, status=403)

    # converte JSON
    try:

        data = json.loads(request.body)

    except json.JSONDecodeError:

        return JsonResponse({"error": "JSON inválido"}, status=400)

    event = data.get("event")

    payment_data = data.get("payment")

    if not payment_data:

        return JsonResponse({"error": "Pagamento não encontrado"}, status=400)

    payment_id = payment_data.get("id")

    try:

        payment = Payment.objects.get(payment_id=payment_id)

    except Payment.DoesNotExist:

        # NÃO retorna erro para o Asaas

        return JsonResponse({"success": True, "ignored": True})

    # pagamento confirmado

    asaas_status = payment_data.get("status")

    if (
        event
        in [
            "PAYMENT_RECEIVED",
            "PAYMENT_CONFIRMED",
        ]
        or asaas_status == "RECEIVED_IN_CASH"
    ):

        # evita processar duas vezes
        if payment.status != "paid":

            payment.status = "paid"

            payment.paid_at = timezone.now()

            payment.save()

            car = payment.car

            car.is_paid = True
            car.is_active = True

            car.set_expiration()

            car.save()

    elif event == "PAYMENT_OVERDUE":

        payment.status = "expired"

        payment.save()

    return JsonResponse({"success": True})
