from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CostomUserAdmin(UserAdmin):

    """Custom User Admin"""

    fieldsets = UserAdmin.fieldsets + (
        (
            "h_Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )
    # list_display = ("username", "email", "gender", "language", "currency", "superhost")
    # list_filter = ("currency", "language", "superhost")


#  admin.site.register(models.User, CostomUserAdmin)  # @admin.register(models.User)나 이걸 사용할수 있다.
