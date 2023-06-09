from django.urls import path, include
from chat import views
from django.contrib.auth.views import LoginView, LogoutView
 
 
urlpatterns = [
    path("", views.base, name="base"),
    path("chatpage/<str:room_name>/", views.chatPage, name="chat-page"),
 
   
    path("login/", views.login_view, name="login-user"),

    path("signup/",views.signup, name = "signup"),
    path("logout/", views.logout_view, name="logout-user"),
    path("home/", views.home, name = "home"),
    path("connect/", views.connect, name = "connect"),
    path("continue_connect/", views.continue_connect, name = "continue_connect"),
    path("disconnect/", views.disconnect, name = "disconnect"),
    path("toggle_online_status/",views.toggle_online_status, name='toggle_online_status'),
]

from chat.routing import websocket_urlpatterns
urlpatterns += websocket_urlpatterns