from django.urls import path
from . import views

urlpatterns = [
    path('api/<path:inputAddr>/', views.getGeocoding),
]