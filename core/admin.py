from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Users)

class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    ordering = ('id', )
    search_fields = ('username', 'email')

@admin.register(Posts)

class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'posted_by')
    ordering = ('id',)
    search_fields = ('posted_by',)

@admin.register(FollowSystem)

class FollowAdmin(admin.ModelAdmin):
    list_display = ['id', 'follower', 'following']
    ordering = ['id']
    search_fields = ['follower', 'following']

@admin.register(Requests)

class RequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'requested_by', 'requested_to']
    ordering = ['id']
    search_fields = ['requested_by', 'requested_to']


@admin.register(Files)

class FilesAdmin(admin.ModelAdmin):
    list_display = ['id']
    ordering = ['id']

@admin.register(Comments)

class CommentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'commented_by']
    ordering = ['id']
    search_fields = ['commented_by']

@admin.register(MessageInstances)

class MessageInstancesAdmin(admin.ModelAdmin):
    list_display = ["id", "type", "message"]
    ordering = ["id"]

@admin.register(Messages)

class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'incoming', 'outgoing')
    ordering = ('id', )
    search_fields = ('incoming', 'outgoing')


@admin.register(Groups)

class GroupsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id']
    search_fields = ['name']

@admin.register(GroupMessage)

class GroupMessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'incoming', 'outgoing')
    ordering = ('id', )
    search_fields = ('incoming', 'outgoing')
