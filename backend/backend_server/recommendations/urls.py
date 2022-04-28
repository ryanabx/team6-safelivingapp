from django.urls import path
from . import views

urlpatterns = [
    path('api/radius/<str:scoreCategory>/<str:initialCity>/<str:stateID>/<str:radiusValue>/<str:minPopulation>/', views.recommendCity),
    path('api/radius/<str:scoreCategory>/<str:initialCity>/<str:stateID>/<str:radiusValue>/<str:minPopulation>/<str:maxPopulation>/', views.recommendCity),
    path('api/radius/<str:scoreCategory>/<str:initialCity>/<str:stateID>/<str:radiusValue>/', views.recommendCity),
    
    path('api/state/<str:scoreCategory>/<str:stateID>/', views.recommendCity),
    path("api/state/<str:scoreCategory>/<str:stateID>/<str:minPopulation>/", views.recommendCity),
    path("api/state/<str:scoreCategory>/<str:stateID>/<str:minPopulation>/<str:maxPopulation>/", views.recommendCity)
]

#http://localhost:8000/recommendations/api/radius/safe-living/tulsa/200
#http://localhost:8000/recommendations/api/state/violent/OK