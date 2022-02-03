from django.urls import path
from . import views

urlpatterns = [
    path('api/<str:city>/<str:state>/', views.get_score),
    path('api/<str:city>/<str:state>/<str:score_type>', views.get_score),
    path('api/<str:city>/<str:state>/<str:score_type>/<str:crime_type>', views.get_score),
]