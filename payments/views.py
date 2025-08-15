from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import requests
from django.conf import settings
from django.shortcuts import redirect
import uuid




class InitializePayment(APIView):
    permission_classes =[
        IsAuthenticated,
    ]

    def post(self,request):
        user = request.user
        url = f"{settings.FLUTTERWAVE_BASE_URL}/payments"

        headers = {
            "Authorization":f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
            "Content-Type":"application/json"
        }

        payload = {
            "tx_ref":str(uuid.uuid4()),
            "amount":"100",
            "currency":"NGN",
            "redirect_url":"http://127.0.0.1:8000/payments/callback/",
            "payment_options": "card, banktransfer",
            "customer": {
                "email": "user@example.com",
                "phonenumber": "08012345678",
                "name": "John Doe"
            },
            "customizations": {
                "title": "My Store",
                "description": "Payment for items in cart"
            }
        }

        response = requests.post(url, json=payload, headers=headers)
        res_data = response.json()
        print(res_data)
        if res_data["status"] == "success":
            return redirect(res_data["data"]["link"])
        return redirect("/payment/error/")



def payment_callback(request):
    status = request.GET.get("status")
    transaction_id = request.GET.get("transaction_id")

    if status == "successful":
        verify_payment(transaction_id)
        return JsonResponse({"message": "Payment successful"})
    else:
        return JsonResponse({"message": "Payment failed"})




def verify_payment(transaction_id):
    url = f"{settings.FLUTTERWAVE_BASE_URL}/transactions/{transaction_id}/verify"
    headers = {"Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"}

    response = requests.get(url, headers=headers)
    res_data = response.json()

    if res_data["status"] == "success" and res_data["data"]["status"] == "successful":
        # Mark order/payment as completed
        return True
    return False
