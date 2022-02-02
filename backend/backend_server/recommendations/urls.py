from django.urls import path
from . import views

urlpatterns = [
    path('api/recommend/<str:initialAddress>/<str:radiusValue>/<str:populationPreference', views.recommendCity),
    path('api/recommend/<str:initialAddress>/<str:radiusValue>', views.recommendCity)
]