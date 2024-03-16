from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="chatHome"),
    path('direct/<int:userid>', chat, name="chat"),
    path('sendmessage', sendmessage, name = "message"),
    path('sendimage', sendImage, name="send-image"),
    path('fetch/<int:userid>', fetch, name = "fetch"),
    path('create/group', createGroup, name="create-group"),
    path('group/<int:groupid>', groupChat, name="group-chat"),
    path('fetch/group/<int:groupid>', fetchGroup, name = "fetchgroup"),
    path('group/sendmessage', groupSendmessage, name="sendGroupMessage"),
    path('group/sendimage', groupSendImage, name="sendGroupImage"),
    path('message/delete/', deleteMessage, name="deleteMessage"),
    path('search', search, name="search")
]
