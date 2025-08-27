from rest_framework import serializers, status

from . import models

from mentors.models import Sessions
from info.models import ExchangeRate

import uuid


class InitializePaymentSerializer(serializers.Serializer):
    session = serializers.PrimaryKeyRelatedField(queryset=Sessions.objects.all())
    
    def validate_session(self,session):
        user = self.context["user"]
        if user != session.mentee:
            raise serializers.ValidationError("This session was not initiated by you.")
        if session.status == "PENDING":
            raise serializers.ValidationError("This session is yet to be accepted by the mentor.")
        #Avoid paying again for an already paid session
        if session.is_paid:
            raise serializers.ValidationError("This session has already been paid for.")
        return session

    def create(self,validated_data):
        session = validated_data.get("session")
        session_prefix = session.mentor.id 
        session_suffix = session.mentee.id 
        transaction_id = f"{session_prefix}{uuid.uuid4()}{session_suffix}"

        initiator = self.context["user"]
        #user_country = initiator.profile.country_code
        user_country = "+234"

        rate = ExchangeRate.objects.filter(country__code=user_country).first()
        if not rate:
            transaction = models.SessionTransactions.objects.create(transaction_id=transaction_id,session=session,initiator=initiator,mentor=session.mentor,amount=session.mentor.profile.session_rate,currency="USD",status="pending")
        else:
            amount = int(session.mentor.profile.session_rate*rate.exchange_rate)
            currency = "NGN"
            transaction = models.SessionTransactions.objects.create(transaction_id=transaction_id,session=session,initiator=initiator,mentor=session.mentor,amount=amount,currency=currency,status="pending")
        return transaction

class StripeInitializePaymentSerializer(serializers.Serializer):
    session = serializers.PrimaryKeyRelatedField(queryset=Sessions.objects.all())

    def validate_session(self,session):
        user = self.context["user"]
        if user != session.mentee:
            raise serializers.ValidationError("This session was not initiated by you.")
        if session.status == "PENDING":
            raise serializers.ValidationError("This session is yet to be accepted by the mentor.")
        #Avoid paying again for an already paid session
        if session.is_paid:
            raise serializers.ValidationError("This session has already been paid for.")
        return session

