from django.contrib import admin

from . import models


@admin.register(models.message)
class MessageAdmin(admin.ModelAdmin):

    """Message Admin Definition"""

    list_display = ("conversation", "__str__", "create")


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """Conversations Admin Definition"""

    list_display = (
        "__str__",
        "count_participants",
        "count_messages",
    )
