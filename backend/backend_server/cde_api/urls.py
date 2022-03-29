from django.urls import path
from . import views

urlpatterns = [
    path('api/<str:agency>/<int:fromDate>/<int:toDate>/', views.api_get_crime_data),
]