from django.urls import path
from . import views

urlpatterns = [
    path('new_user/<str:username>/<str:email>/<str:password>/', views.newUser),
    path('change_password/<str:username>/<str:password>/<str:newpassword>/', views.changePassword),
]