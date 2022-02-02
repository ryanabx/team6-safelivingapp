from django.urls import path
from . import views

urlpatterns = [
    path('api/submitReview/<str:city>/<str:state>/<str:rating>/<str:text>/', views.submitReview),
    path('api/getReview/<str:city>/<str:state>/', views.getReview),
]