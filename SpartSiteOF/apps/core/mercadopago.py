import mercadopago

sdk = mercadopago.SDK(
    "TEST-6876772324356892-051922-12f69d7db745a2308572b7a9904195e7-236073880"
)


def procesar_pago_tarjeta(request):
    payment_data = {
        "transaction_amount": float(request.POST.get("transaction_amount")),
        "token": request.POST.get("token"),
        "description": request.POST.get("description"),
        "installments": int(request.POST.get("installments")),
        "payment_method_id": request.POST.get("payment_method_id"),
        "payer": {
            "email": request.POST.get("cardholderEmail"),
            "identification": {
                "type": request.POST.get("identificationType"),
                "number": request.POST.get("identificationNumber"),
            },
            "first_name": request.POST.get("cardholderName"),
        },
    }

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]

    return payment


def procesar_pago_ticket(request):
    payment_data = {
        "transaction_amount": float(request.POST.get("transaction_amount")),
        "description": "Título do produto",
        "payment_method_id": "bolbradesco",
        "payer": {
            "email": request.POST.get("payer_email"),
            "first_name": request.POST.get("payer_first_name"),
            "last_name": request.POST.get("payer_last_name"),
            "identification": {
                "type": request.POST.get("identification_type"),
                "number": request.POST.get("identification_number"),
            },
            "address": {
                "zip_code": request.POST.get("zip_code"),
                "street_name": request.POST.get("street_name"),
                "street_number": request.POST.get("street_number"),
                "neighborhood": request.POST.get("neighborhood"),
                "city": request.POST.get("city"),
                "federal_unit": request.POST.get("federal_unit"),
            },
        },
    }
    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]

    return payment
