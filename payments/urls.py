from django.urls import path
from . import views

urlpatterns = [
    path("initiate/",views.FLWInitializePaymentView.as_view(),name="Initiate_payment"),
    path("callback/",views.FLWPaymentCallBack.as_view(),name="Payment-Callback"),
]
