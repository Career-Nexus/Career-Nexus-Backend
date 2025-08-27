from django.urls import path
from . import views

urlpatterns = [
    path("flutterwave/initiate/",views.FLWInitializePaymentView.as_view(),name="Initiate_payment"),
    path("callback/",views.FLWPaymentCallBack.as_view(),name="Payment-Callback"),

    path("stripe/initiate/",views.StripeCreateCheckoutView.as_view(),name="stripe-Initiate-Payment"),

    path("test/redirect/",views.TestRedirect.as_view(),name="Test-Redirect"),
]
