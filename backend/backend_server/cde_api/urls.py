from django.urls import path
from . import views

urlpatterns = [
    path('cdedata/getdata/<str:agency>/<int:fromDate>/<int:toDate>/', views.getStuff),
]