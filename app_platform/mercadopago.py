import mercadopago

sdk = mercadopago.SDK("SEU_ACCESS_TOKEN")

payment_data = {
    "items": [
        {
            "title": "Anúncio Premium",
            "quantity": 1,
            "currency_id": "BRL",
            "unit_price": 19.90
        }
    ]
}

payment_response = sdk.preference().create(payment_data)

print(payment_response)