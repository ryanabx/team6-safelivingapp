from django.urls import path
from . import views

urlpatterns = [
    path('api/walkscore/<str:lat>/<str:lon>/<str:address>', views.getWalkScore),
]