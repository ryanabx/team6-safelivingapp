from django.urls import path
from . import views

urlpatterns = [
    path('api/costbyaddr/<str:addr>/', views.getCostOfLiving),
]