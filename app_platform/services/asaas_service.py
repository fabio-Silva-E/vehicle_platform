import requests

from django.conf import settings
from datetime import date, timedelta


class AsaasService:

    BASE_URL = "https://sandbox.asaas.com/api/v3"

    @classmethod
    def create_pix_payment(cls, car):

        headers = {
            "access_token": settings.ASAAS_API_KEY,
            "Content-Type": "application/json"
        }

        customer_payload = {
            "name": car.owner.username,
            "email": car.owner.email,
            "cpfCnpj": car.owner.cpf_cnpj
        }

        customer_response = requests.post(
            f"{cls.BASE_URL}/customers",
            json=customer_payload,
            headers=headers
        )

        customer_data = customer_response.json()


        if "id" not in customer_data:
            raise Exception(
                f"Erro ao criar cliente: {customer_data}"
            )

        customer_id = customer_data["id"]

        payment_payload = {
            "customer": customer_id,
            "billingType": "PIX",
            "value": float(car.plan.price),
            "dueDate": str(date.today() + timedelta(days=1)),
            "description": f"Pagamento anúncio {car.model}"
        }

        payment_response = requests.post(
            f"{cls.BASE_URL}/payments",
            json=payment_payload,
            headers=headers
        )

        payment_data = payment_response.json()


        # 🔥 VALIDAÇÃO IMPORTANTE
        if "id" not in payment_data:
            raise Exception(
                f"Erro ao criar pagamento: {payment_data}"
            )

        payment_id = payment_data["id"]

        pix_response = requests.get(
            f"{cls.BASE_URL}/payments/{payment_id}/pixQrCode",
            headers=headers
        )

        pix_data = pix_response.json()

        return {
            "payment": payment_data,
            "pix": pix_data
        }

    @classmethod
    def get_payment(cls, payment_id):

        headers = {
            "access_token": settings.ASAAS_API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.get(
            f"{cls.BASE_URL}/payments/{payment_id}",
            headers=headers
        )

        return response.json()

    @classmethod
    def simulate_pix_payment(cls, payment_id, value):

        headers = {
            "access_token": settings.ASAAS_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "paymentDate": str(date.today()),
            "value": float(value)
        }

        response = requests.post(
            f"{cls.BASE_URL}/payments/{payment_id}/receiveInCash",
            json=payload,
            headers=headers
        )

        return response.json()