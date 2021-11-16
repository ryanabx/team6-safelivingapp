from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.
def newUser(request, username, email, password):
    user = User.objects.create_user(username, email, password)
    user.save()
    # user = User.objects.get(username = username)
    # if user is None:
        
    #     return True
    # else:
    #     return False
    
def changePassword(request, username, password, newpassword):
    user = User.objects.get(username = username)
    user = authenticate(username = username, password = password)
    if user is not None:
        user.set_password(newpassword)
        user.save()