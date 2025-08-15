from django.urls import path
from . import views

urlpatterns = [
    path("initiate/",views.initialize_payment,name="Initiate_payment"),
    path("callback/",views.payment_callback,name="Payment-Callback"),
]
