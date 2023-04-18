from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Interest(models.Model):
    name = models.CharField(max_length=50,unique=True)

class User(AbstractUser):
    username = models.CharField(max_length=50,unique =True )
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    interests = models.ManyToManyField(Interest)

    is_online = models.BooleanField(default=True)
    
    
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='chat_users'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='chat_users'
    )

# FOOD = 'Food'
# MOVIES = 'Movies'

# TRAVEL = 'Travel'

# Interest.objects.create(name=FOOD)
# Interest.objects.create(name=MOVIES)
# Interest.objects.create(name=TRAVEL)
# class Interest(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name

# FOOD = 'Food'
# MOVIES = 'Movies'
# TRAVEL = 'Travel'

# Interest.objects.create(name=FOOD)
# Interest.objects.create(name=MOVIES)
# Interest.objects.create(name=TRAVEL)

class Connection(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections2')
    connected = models.BooleanField(default=False)
    online = models.BooleanField(default=False)