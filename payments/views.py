from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

import requests
from django.conf import settings
from django.shortcuts import redirect
import uuid

from payments import serializers




class FLWInitializePaymentView(APIView):
    permission_classes =[
        IsAuthenticated,
    ]

    def post(self,request):
        user = request.user
        serializer = serializers.InitializePaymentSerializer(data=request.data,context={"user":user})
        if serializer.is_valid(raise_exception=True):
            transaction = serializer.save()

            initiator_phone_number = f"{transaction.initiator.profile.country_code}{transaction.initiator.profile.phone_number}"
            initiator_name = f"{transaction.initiator.profile.first_name} {transaction.initiator.profile.last_name}"

            url = f"{settings.FLUTTERWAVE_BASE_URL}/payments"

            headers = {
                "Authorization":f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
                "Content-Type":"application/json"
            }

            payload = {
                "tx_ref":transaction.transaction_id,
                "amount":transaction.amount,
                "currency":transaction.currency,
                "redirect_url":"http://127.0.0.1:8000/payments/callback/",
                "payment_options": "card, banktransfer",
                "customer": {
                    "email": transaction.initiator.email,
                    "phonenumber": initiator_phone_number,
                    "name": initiator_name,
                },
                "customizations": {
                    "title": "Career Nexus",
                    "description": "Payment for Mentorship"
                }
            }

            response = requests.post(url, json=payload, headers=headers)
            res_data = response.json()
            if res_data["status"] == "success":
                return Response({"payment link":res_data["data"]["link"]},status=status.HTTP_200_OK)
                #return redirect(res_data["data"]["link"])
            #return redirect("/payment/error/")
            return Response({"error":"Failed to initialize payment"},status=status.HTTP_503_SERVICE_UNAVAILABLE)



class FLWPaymentCallBack(APIView):
    permission_classes = [
        AllowAny,
    ]
    def get(self,request):
        status = request.query_params.get("status")
        transaction_id = request.query_params.get("transaction_id")
        tx_ref = request.query_params.get("tx_ref")
        container = [status,transaction_id,tx_ref]
        for item in container:
            if not item:
                return Response({"Error":"Invalid Payment References"},status=status.HTTP_400_BAD_REQUEST)
        if status == "successful":
            verify_payment(transaction_id)
            return Response({"message": "Payment successful"})
        else:
            return Response({"message": "Payment failed"},status=status.HTTP_400_BAD_REQUEST)




def verify_payment(transaction_id):
    url = f"{settings.FLUTTERWAVE_BASE_URL}/transactions/{transaction_id}/verify"
    headers = {"Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"}

    response = requests.get(url, headers=headers)
    res_data = response.json()

    if res_data["status"] == "success" and res_data["data"]["status"] == "successful":
        #TODO Write algorithm to mark session as paid
        return True
    return False
