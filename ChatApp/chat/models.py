from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Model for user interests
class Interest(models.Model):
    name = models.CharField(max_length=50, unique=True)

# Custom User model which inherits from Django's AbstractUser model
class User(AbstractUser):
    # Custom fields for user profile
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    interests = models.ManyToManyField(Interest) # A user can have multiple interests
    
    is_online = models.BooleanField(default=True) # Indicates if user is currently online
    
    # User can belong to multiple groups
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='chat_users'
    )
    
    # User can have multiple permissions
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='chat_users'
    )

# Model for user connections
class Connection(models.Model):
    # A connection is between two users
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections2')
    room_name = models.CharField(max_length=50)
    connected_at = models.DateTimeField(auto_now_add=True)