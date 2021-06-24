from django.contrib import admin

from . import models


@admin.register(models.message)
class MessageAdmin(admin.ModelAdmin):

    """Message Admin Definition"""

    pass


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """Conversations Admin Definition"""

    pass
