from django.urls import path
from . import views

urlpatterns = [
    path('api/<str:city>/<str:state>/', views.getScore),
    path('api/<str:city>/<str:state>/<str:crime_type>', views.getScore),
    path('api/<str:ORI>/', views.getScorebyORI),
]