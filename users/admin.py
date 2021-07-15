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

    list_display = UserAdmin.list_display + (
        "gender",
        "language",
        "currency",
        "superhost",
    )
    # list_display = ("username", "email", "gender", "language", "currency", "superhost")
    # list_filter = ("currency", "language", "superhost")


#  admin.site.register(models.User, CostomUserAdmin)  # @admin.register(models.User)나 이걸 사용할수 있다.


# 장고의 UserAdmin 에 기본적으로 설정이 들어가 있으므로 그걸 상속받은후 h_Custom Profile을 추가해준다.
# class CostomUserAdmin(admin.ModelAdmin):
