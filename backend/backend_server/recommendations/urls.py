from django.urls import path
from . import views

urlpatterns = [
    path('api/<str:initialAddress>/<str:radiusValue>/<str:minPopulation>', views.recommendCity),
    path('api/<str:initialAddress>/<str:radiusValue>/<str:minPopulation>/<str:maxPopulation>', views.recommendCity),
    path('api/<str:initialAddress>/<str:radiusValue>', views.recommendCity)
]