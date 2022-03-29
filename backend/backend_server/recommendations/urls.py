from django.urls import path
from . import views

urlpatterns = [
    path('api/radius/<str:initialAddress>/<str:radiusValue>/<str:minPopulation>', views.recommendCity),
    path('api/radius/<str:initialAddress>/<str:radiusValue>/<str:minPopulation>/<str:maxPopulation>', views.recommendCity),
    path('api/radius/<str:initialAddress>/<str:radiusValue>', views.recommendCity),
    
    path('api/state/<str:stateID>', views.recommendCity),
    path("api/state/<str:stateID>/<str:minPopulation>", views.recommendCity),
    path("api/state/<str:stateID>/<str:minPopulation>/<str:maxPopulation>", views.recommendCity)
]