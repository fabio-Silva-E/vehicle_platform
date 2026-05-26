from datetime import timedelta

from django.utils import timezone

from .models import Payment


def delete_expired_unpaid_ads():

    limit_date = timezone.now() - timedelta(hours=24)

    expired_payments = Payment.objects.filter(
        status="pending",
        created_at__lte=limit_date
    )

    for payment in expired_payments:



        payment.car.delete()