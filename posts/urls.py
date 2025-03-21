from . import views
from django.urls import path


urlpatterns= [
            path("",views.PostView.as_view(),name="Add-View-Posts"),
        ]
