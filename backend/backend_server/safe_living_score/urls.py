from django.urls import path
from . import views

urlpatterns = [
    path('api/<str:lon>/<str:lat>/<str:radius>', views.getScore),
    path('api/<str:ORI>/', views.getScorebyORI),
]