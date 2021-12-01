from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("users/", views.index, name="user_index"),
    path("login/", views.loginPage, name="login"),
    path("register/", views.registerPage, name="register"),
    path("logout/", views.logoutUser, name="logout"),
    path("createProfile/", views.userCreateProfile, name="createProfile"),
    path("follow/<int:id>/", views.userFollow, name="follow"),
    path("userProfile/<int:id>/", views.userProfile, name="userProfile"),
]
