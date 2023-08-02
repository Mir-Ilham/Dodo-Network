from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    
    path("profile/<str:pk>/", views.userProfile, name="user-profile"),
    path("update-user/", views.updateUser, name="update-user"),
    
    path("room/<str:pk>/", views.room, name="room"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<str:pk>/", views.updateRoom, name="update-room"),
    path("delete-room/<str:pk>/", views.deleteRoom, name="delete-room"),

    path("delete-message/<str:pk>/", views.deleteMessage, name="delete-message"),

    path("create-post/", views.createPost, name="create-post"),
    path("update-post/", views.updatePost, name="update-post"),
    path("delete-post/", views.deletePost, name="delete-post"),

    path("topics/", views.listTopics, name="topics"),
    path("activity/", views.showActivity, name="activity"),
]