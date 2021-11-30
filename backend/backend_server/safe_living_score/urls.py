from django.urls import path
from . import views

urlpatterns = [
    path('api/<str:lat>/<str:lon>/<str:radius>/', views.getScore),
    path('api/<str:lat>/<str:lon>/<str:radius>/<str:crime_type>', views.getScore),
    path('api/<str:ORI>/', views.getScorebyORI),
]