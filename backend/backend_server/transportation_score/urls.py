from django.urls import path
from . import views

urlpatterns = [
    path('api/walkscore/<str:lon>/<str:lat>/<str:address>', views.getWalkScore),
]