from django.urls import path
from . import views

urlpatterns = [
    path('api/costbylonlat/<str:lon>/<str:lat>/', views.getCostOfLiving),
]