# Import necessary modules and models
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User, Interest, Connection
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import random

# Define a view for the base page
def base(request):
    return render(request, 'base.html')

# Define a view for the chat page
def chatPage(request, room_name, *args, **kwargs):
    # Check if user is authenticated, redirect to login page if not
    if not request.user.is_authenticated:
        return redirect("login-user")
    user = request.user
    # Extract the other user's id from the room name
    other_user_id = room_name.split('_')
    # Determine the other user based on the id and the current user
    if (user.id == int(other_user_id[0])):
        other_user = User.objects.get(id=other_user_id[1])
    else:
        other_user = User.objects.get(id=other_user_id[0])
    # Create a context dictionary to pass to the template
    context = {
        'user': user,
        'other_user': other_user,
        'room_name': room_name,
    }
    return render(request, "chat/chatPage.html", context)

# Define a view for the signup page
def signup(request):
    # Handle form submission
    if request.method == 'POST':
        # Extract user information from the form
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST['gender']
        country = request.POST['country']
        password = request.POST['password']
        interests = request.POST.getlist('interests')
        # Create a user object with the extracted information
        user = User.objects.create_user(username=full_name, full_name=full_name, email=email, phone=phone, gender=gender, country=country, password=password)
        user.save()
        # Add the selected interests to the user's profile
        for interest_id in interests:
            interest = Interest.objects.get(pk=interest_id)
            user.interests.add(interest) 
        # Redirect the user to the login page
        return redirect('login-user')
    else:
        # Retrieve all interests to display them in the form
        interests = Interest.objects.all()
        return render(request, 'signup.html', {'interests': interests})

# Define a view for the login page
def login_view(request):
    # Handle form submission
    if request.method == 'POST':
        email_or_phone = request.POST['email_or_phone']
        password = request.POST['password']
        # Try to retrieve a user object using the email or phone provided
        try:
            user_ = User.objects.get(email=email_or_phone)
        except User.DoesNotExist:
            try:
                user_ = User.objects.get(phone=email_or_phone)
            except User.DoesNotExist:
                user_ = None
        # Authenticate the user if they exist and redirect to home page
        if user_ is not None:
            user = authenticate(request, username=user_.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'chat/LoginPage.html', {'error': 'Invalid login credentials.'})
    # Display the login page
    return render(request, 'chat/LoginPage.html')
   
# Import necessary modules
from django.db.models import Q
import random

# Define a view for the home page
def home(request):
    # Get the current user object from the request
    user = request.user
    # Get all connections that the user is a part of and that are currently connected or online
    connections = Connection.objects.filter(user1=user, connected=True) | Connection.objects.filter(user2=user, connected=True)
    online = Connection.objects.filter(user1=user, online=True) | Connection.objects.filter(user2=user, online=True)
    # Return the rendered template for the home page, passing in the user, connections, and online objects as context
    return render(request, 'home.html', {'user': user, 'connections': connections, 'online': online})

# Define a view for connecting two users
def connect(request):
    # Get the current user object from the request and set their online status to True
    user = request.user
    user.is_online = True
    user.save()

    # Get all interests of the current user
    interests = user.interests.all()
    # Find other users who have at least one shared interest with the current user and are online
    other_users = User.objects.filter(~Q(id=user.id), interests__in=interests, is_online=True)
    # If no other users are found with shared interests and online, find all online users
    if not other_users:
        other_users = User.objects.filter(~Q(id=user.id), is_online=True)

    # If there are other users available, randomly choose one to connect with
    if other_users:
        other_user = random.choice(other_users)
        other_user.is_online = False
        other_user.save()
        # Generate a room name for the chat between the two users and redirect to the chat page for that room
        room_name = f"{min(user.id, other_user.id)}_{max(user.id, other_user.id)}"
        return redirect('chat-page', room_name=room_name)

    # If no other users are available, redirect back to the home page
    return redirect('home')


# Define a view for disconnecting from a chat
def disconnect(request):
    # Get the current user object from the request and their connection object
    user = request.user
    connection = user.connection
    # Determine which user in the connection is the current user and set their online status to False
    if connection.user1 == user:
        connection.user1_online = False
        connection.user1 = None
    else:
        connection.user2_online = False
        connection.user2 = None
    # Save the changes to the connection object and redirect back to the home page
    connection.save()
    return redirect('home')

# Define a view for toggling the online status of the current user
def toggle_online_status(request):
    # Get the current user object from the request and toggle their online status
    user = request.user
    user.is_online = not user.is_onlineer.is_online
    user.save()
    return redirect('home')

def logout_view(request):
    # Log the user out (i.e., remove their session from the server)
    logout(request)
    
    # Redirect the user to the 'base' page
    return redirect('base')