from django.urls import path
from . import views
from . import bookmarking

urlpatterns = [
    path('new_user/<str:username>/<str:email>/<str:password>/', views.newUser),
    path('change_password/<str:username>/<str:password>/<str:newpassword>/', views.changePassword),
    path('api/get_bookmarks/<str:user>/', bookmarking.getBookmarks),
    path('api/del_bookmark/<str:user>/<str:address>/', bookmarking.delBookmark),
    path('api/add_bookmark/<str:user>/<str:address>/', bookmarking.addBookmark)
]