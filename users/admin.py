from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from rooms.models import Room as room_model


class RoomInline(admin.StackedInline):  # 8.6-2
    model = room_model

    filter_horizontal = (  # 2 참조 # 이렇게도 먹는다!!
        "amenities",
        "facilities",
        "house_rules",
    )


@admin.register(models.User)
class CostomUserAdmin(UserAdmin):

    """Custom User Admin"""

    inlines = (RoomInline,)  # 8.6-2

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
                    "email_verified",
                    "login_method",
                )
            },
        ),
    )

    # list_display = UserAdmin.list_display + (
    #     "gender",
    #     "language",
    #     "currency",
    #     "superhost",
    # )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
        "login_method",
    )

    list_filter = UserAdmin.list_filter + ("superhost",)
    # list_filter = ("currency", "language", "superhost")


#  admin.site.register(models.User, CostomUserAdmin)
# # @admin.register(models.User)나 이걸 사용할수 있다.


# 장고의 UserAdmin 에 기본적으로 설정이 들어가 있으므로 그걸 상속받은후 h_Custom Profile을 추가해준다.
# class CostomUserAdmin(admin.ModelAdmin):
