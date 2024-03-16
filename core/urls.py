from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = "home"),
    path('details/<str:username>/', details, name="details"),
    path('follow/', follow, name="follow"),
    path('unfollow/', unfollow, name="unfollow"),
    path('remove/request/follow', derequest, name="remfollowreq"),
    path('request/action/', requestAction, name="requestaction"),
    path('post/create/', createPost, name="createpost"),
    path('post/create/success/', createsuccess, name="createpostsuccess"),
    path('post/like/', likePost, name="like"),
    path('post/dislike/', dislikePost, name="dislike"),
    path('post/display/<int:postid>', displayPost, name="displayPost"),
    path('post/comment/', commentPost, name="sendcomment"),
    path('logout', logout, name="logout")
]
