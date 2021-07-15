from django.contrib import admin
from . import models


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = ("name", "create", "update")


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        (
            "Time",
            {"fields": ("check_in", "check_out", "instant_book")},
        ),
        (
            "Spaces",
            {"fields": ("gueste", "beds", "bedrooms", "baths")},
        ),
        (
            "More About the Space",
            {
                "classes": ("collapse",),  # 목록 숨김 그외에 여러기능들이 있다.
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        (
            "Last Details",
            {"fields": ("host",)},
        ),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "gueste",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
    )

    ordering = ("name", "price")

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    search_fields = ("city", "^host__username")  # 1 참조

    filter_horizontal = (  # 2 참조
        "amenities",
        "facilities",
        "house_rules",
    )

    def count_amenities(self, obj):  # 첫번째인자 : 현 클래스 자체 두번째 인자 : 표시될 현제 row
        # print(obj)  # 집입니다요
        # print(obj.amenities)  # rooms.Amenity.None
        # print(obj.amenities.all())  # <QuerySet [<Amenity: Washer>]>
        # print(obj.amenities.count())  # 1
        return obj.amenities.count()

    count_amenities.short_description = "시설들!!"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""

    pass


"""   1
    여러 검색방법이 있다. "^city",  "=city" 등등
    "host__username" self.host.username 를 검색헤서 사용한다. 
"""

"""   2
    ManyToManyField 에서만 작동한다.
    어드민 에서      
    샤워
    wifi     +  
    washer

    부분을  검색과 선택이 되는 화면으로 바꿔준다. 
"""
