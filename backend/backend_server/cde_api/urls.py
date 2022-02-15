from django.urls import path
from . import views

urlpatterns = [
    path('api/<str:agency>/<int:fromDate>/<int:toDate>/', views.get_crime_data),
]