from django.urls import path
from . import views

urlpatterns = [
    path('api/<str:lat>/<str:lon>/<str:radius>/<str:type>', views.getAmenities),
]