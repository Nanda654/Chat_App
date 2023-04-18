from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User, Interest, Connection
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import random

def base(request):
    return render(request, 'base.html')

def chatPage(request, room_name, *args, **kwargs):
    print('chatpage')
    if not request.user.is_authenticated:
        return redirect("login-user")
    user = request.user
    other_user_id = room_name.split('_')
    print(f'{type(user.id)},{other_user_id[0]},{type(other_user_id[1])}')
    if (user.id== int(other_user_id[0])):
        other_user = User.objects.get(id=other_user_id[1])
    else:
        other_user = User.objects.get(id=other_user_id[0])

    context = {
        'user': user,
        'other_user': other_user,
        'room_name': room_name,
    }
    return render(request, "chat/chatPage.html", context)


def signup(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST['gender']
        country = request.POST['country']
        password = request.POST['password']
        interests = request.POST.getlist('interests')
        # Create the user object and save it to the database
        user = User.objects.create_user(username=full_name,full_name=full_name, email=email, phone=phone, gender=gender, country=country, password=password)
        user.save()
        # Add the selected interests to the user's profile
        for interest_id in interests:
            interest = Interest.objects.get(pk=interest_id)
            user.interests.add(interest) 
        
        return redirect('login-user')
    else:
        interests=[]
        interests = Interest.objects.all()
        return render(request, 'signup.html', {'interests': interests})
        

def login_view(request):
    if request.method == 'POST':
        email_or_phone = request.POST['email_or_phone']
        password = request.POST['password']
        # print(f"Username: {email_or_phone}, Password: {password}")
        # import pdb; pdb.set_trace()
        try:
            user_ = User.objects.get(email=email_or_phone)
        except User.DoesNotExist:
            try:
                user_ = User.objects.get(phone=email_or_phone)
            except User.DoesNotExist:
                user_ = None
        if user_ is not None:
            user = authenticate(request,  username=user_.username, password=password)
            # print(f"authentication: {user}")
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'chat/LoginPage.html', {'error': 'Invalid login credentials.'})
    
    return render(request, 'chat/LoginPage.html')
   
def home(request):
    user = request.user
    connections = Connection.objects.filter(user1=user, connected=True) | Connection.objects.filter(user2=user, connected=True)
    online = Connection.objects.filter(user1=user, online=True) | Connection.objects.filter(user2=user, online=True)
    return render(request, 'home.html', {'user': user, 'connections': connections, 'online': online})

from django.db.models import Q
import random


# @login_required
def connect(request):
    user = request.user
    user.is_online = True
    user.save()

    interests = user.interests.all()
    other_users = User.objects.filter(~Q(id=user.id), interests__in=interests, is_online=True)
    if not other_users:
        other_users = User.objects.filter(~Q(id=user.id), is_online=True)

    if other_users:
        other_user = random.choice(other_users)
        other_user.is_online = False
        other_user.save()
        room_name = f"{min(user.id, other_user.id)}_{max(user.id, other_user.id)}"
        return redirect('chat-page', room_name=room_name)

    return redirect('home')

# @login_required
def chat(request, room_name):
    user = request.user
    other_user_id = room_name.split('_')[1]
    other_user = User.objects.get(id=other_user_id)

    context = {
        'user': user,
        'other_user': other_user,
        'room_name': room_name,
    }

    return render(request, 'chatpage.html', context)

# @login_required

# @login_required
def disconnect(request):
    user = request.user
    connection = user.connection
    if connection.user1 == user:
        connection.user1_online = False
        connection.save()
        connection.user1 = None
    else:
        connection.user2_online = False
        connection.save()
        connection.user2 = None
    connection.save()
    return redirect('home')

def toggle_online_status(request):
    user = request.user
    user.is_online = not user.is_online
    user.save()
    return redirect('home')

def logout_view(request):
    
    logout(request)
    return redirect('base')