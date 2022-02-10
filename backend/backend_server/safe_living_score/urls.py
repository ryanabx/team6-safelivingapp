from django.urls import path
from . import views

urlpatterns = [
    path('api/<str:city>/<str:state>/', views.get_score),
]