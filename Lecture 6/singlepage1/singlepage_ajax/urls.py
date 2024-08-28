from django.urls import path, include
from . import views

urlpatterns = [
    path("", view=views.index, name="index"),
    path("states/<str:state_of_matter>", view=views.state_response, name="state_response")
]
