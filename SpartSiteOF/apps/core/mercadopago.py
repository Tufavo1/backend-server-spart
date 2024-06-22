import mercadopago

sdk = mercadopago.SDK(
    "TEST-6876772324356892-051922-12f69d7db745a2308572b7a9904195e7-236073880"
)


def create_payment(request):
    try:
        payment_data = {
            "transaction_amount": float(request.POST.get("transactionAmount")),
            "token": request.POST.get("token"),
            "description": request.POST.get("description"),
            "installments": int(request.POST.get("installments")),
            "payment_method_id": request.POST.get("paymentMethodId"),
            "payer": {
                "email": request.POST.get("email"),
                "identification": {
                    "type": request.POST.get("identificationType"),
                    "number": request.POST.get("identificationNumber"),
                },
            },
        }
        payment_response = sdk.payment().create(payment_data)
        return payment_response["response"]
    except Exception as e:
        return {"status": "failure", "message": str(e)}
