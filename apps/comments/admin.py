from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["product","user1","comment","is_active",]
    list_editable = ["is_active"]
