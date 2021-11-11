from django.urls import path
from . import views

urlpatterns = [
    path('api/<str:lon>/<str:lat>/<str:radius>/<str:type>', views.getAmenities),
]