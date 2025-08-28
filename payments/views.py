from json import load
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import models

import requests
from django.conf import settings
from django.shortcuts import redirect
import uuid

import stripe


from payments import serializers




stripe.api_key=settings.STRIPE_SECRET_KEY





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
                "redirect_url":f"{settings.HOST_URL}/payments/callback/",
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
            return Response({"error":"Failed to initialize payment"},status=status.HTTP_503_SERVICE_UNAVAILABLE)



class FLWPaymentCallBack(APIView):
    permission_classes = [
        AllowAny,
    ]
    def get(self,request):
        transact_status = request.query_params.get("status")
        transaction_id = request.query_params.get("transaction_id")
        tx_ref = request.query_params.get("tx_ref")
        container = [transact_status,transaction_id,tx_ref]
        for item in container:
            if not item:
                return Response({"Error":"Invalid Payment References"},status=status.HTTP_400_BAD_REQUEST)

        models.TransactionCallbacks.objects.create(tx_ref=tx_ref,transaction_id=transaction_id)

        if transact_status == "successful":
            verification = verify_payment(transaction_id,tx_ref)
            if verification:
                return redirect("https://master.dnoqikexgmm2j.amplifyapp.com/payment-success/")
        
        return redirect("https://master.dnoqikexgmm2j.amplifyapp.com/payment-failed/")





def verify_payment(transaction_id,tx_ref):
    url = f"{settings.FLUTTERWAVE_BASE_URL}/transactions/{transaction_id}/verify"
    headers = {"Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"}

    response = requests.get(url, headers=headers)
    res_data = response.json()

    if res_data["status"] == "success" and res_data["data"]["status"] == "successful":
        session_transaction = models.SessionTransactions.objects.filter(transaction_id=tx_ref).first()
        #Defense again fraudulent API calls with previously verified credentials
        if not session_transaction:
            return False
        elif session_transaction.status != "pending":
            return False
        else:
            session_transaction.status = "successful"
            session_transaction.session.is_paid = True
            session_transaction.session.save()
            session_transaction.save()
            return True
    return False


class StripeRedirect(APIView):
    permission_classes = [
        AllowAny,
    ]
    def get(self,request):
        session_id = request.query_params.get("session_id")
        if not session_id:
            return redirect("https://master.dnoqikexgmm2j.amplifyapp.com/payment-failed/")
        else:
            #Ensure that the session_id exists in the database with a pending status
            transaction = models.StripeTransactions.objects.filter(transaction_id=session_id,status="pending").first()
            if not transaction:
                return redirect("https://master.dnoqikexgmm2j.amplifyapp.com/payment-failed/")
            else:
                session = stripe.checkout.Session.retrieve(session_id,expand=["payment_intent"])
                if session.payment_status == "paid":
                    transaction.status = "successful"
                    transaction.save()
                    transaction.session.is_paid = True
                    transaction.session.save()
                    return redirect("https://master.dnoqikexgmm2j.amplifyapp.com/payment-success/")
                else:
                    return redirect("https://master.dnoqikexgmm2j.amplifyapp.com/payment-failed/")




class StripeCreateCheckoutView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self,request):
        user = request.user
        serializer = serializers.StripeInitializePaymentSerializer(data=request.data,context={"user":user})
        if serializer.is_valid(raise_exception=True):
            session = serializer.validated_data.get("session")
            amount = session.mentor.profile.session_rate

            DOMAIN_NAME = settings.HOST_URL

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data":{
                        "currency":"usd",
                        "product_data":{
                            "name":"Payment for Mentorship Session."
                        },
                        "unit_amount":amount*100
                    },
                    "quantity":1
                }],
                mode="payment",
                success_url=f"{DOMAIN_NAME}/payments/test/redirect/?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{DOMAIN_NAME}/payments/test/redirect/"
            )

            models.StripeTransactions.objects.create(transaction_id=checkout_session.id,session=session,initiator=session.mentee,amount=amount)
        return Response({"session_id":checkout_session.id,"url":checkout_session.url})
