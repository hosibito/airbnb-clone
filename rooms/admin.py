from django.contrib import admin

from django.utils.html import mark_safe

from . import models


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = ("name", "create", "update", "used_by")

    def used_by(self, obj):
        return obj.room_set.count()


class PhotoInline(admin.TabularInline):  # 노트 8.6 -2 참조 (어드민 내부에 다른 어드민을 추가한다.)

    model = models.Photo

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    inlines = (PhotoInline,)   # 노트 8.6 -2 참조

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "city", "price")},
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
        "count_amenities",  # 2 manytomanyfield 는 list_display에 표시할수 없으므로 함수로 만들어 표시한다.
        "count_photos",
        "total_rating",
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

    raw_id_fields = ("host",)  # 노트 8.6 참조

    search_fields = ("city", "^host__username")  # 1 참조

    filter_horizontal = (  # 2 참조
        "amenities",
        "facilities",
        "house_rules",
    )

    def save_model(self, request, obj, form, change):  # note 8.8 참조
        # print(f"obj : {obj}")           # obj : 집입니다요
        # print(f"change : {change}")     # change : True
        # print(f"form : {form}")         # form : <tr><th><label for="id_name">Name:</l..

        return super().save_model(request, obj, form, change)

    def count_amenities(self, obj):  # 3 첫번째인자 : 현 클래스 자체 두번째 인자 : 표시될 현제 row
        # print(obj)  # 집입니다요
        # print(obj.amenities)  # rooms.Amenity.None
        # print(obj.amenities.all())  # <QuerySet [<Amenity: Washer>]>
        # print(obj.amenities.count())  # 1
        return obj.amenities.count()

    count_amenities.short_description = "시설들!!"

    def count_photos(self, obj):
        # print(obj.photo_set.count())  # 4 참조
        return obj.photo_set.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):    # 노트 8.5참조
        return mark_safe(f"<img height='70px' src='{obj.file.url}' />")
    get_thumbnail.short_description = "썸네일"


# ===============================================================================================================
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


"""  4
#7.0  #7.1  볼것.. Django ORM!!!!
python manage.py shell

from users.models import User

User.objects    # <django.contrib.auth.models.UserManager object at 0x00000248444A9E20>

User.objects.all()  # <QuerySet [<User: hosibito>, <User: yamizora>]>

all_user = User.objects.all()
all_user.filter(superhost=True)

hosibito = User.objects.get(username="hosibito")
print(hosibito)   # hosibito

vars(hosibito)   # {'_state': <django.db.models.base.ModelState object at 0x000002484488B520>, 'id': 1, 'password': 'pbkdf2_sha256$150000$dCwG6TVW7TLD$ngqd9ncM+37puGD2qj0Dv1Fz4aE+415IBmSy5gCm6G0=', 'last_login': datetime.datetime(2021, 7, 15, 6, 1, 11, 968872, tzinfo=<UTC>), 'is_superuser': True, 'username': 'hosibito', 'first_name': '', 'last_name': '', 'email': '', 'is_staff': True, 'is_active': True, 'date_joined': datetime.datetime(2021, 6, 7, 5, 43, 50, tzinfo=<UTC>), 'avatar': '', 'gender': 'male', 'bio': '', 'birthdate': datetime.date(2020, 4, 14), 'language': 'kr', 'currency': 'krw', 'superhost': True}
dir(hosibito)   # ['CURRENCY_CHOICES', 'CURRENCY_KRW', 'CURRENCY_USD', 'DoesNotExist', 'EMAIL_FIELD', 'GENDER_CHOICES', 'GENDER_FRMALE', 'GENDER_MALE', 'GENDER_OTHER', 'LANGUAGE_CHOICES', 'LANGUAGE_ENGLISH', 'LANGUAGE_KOREAN', 'Meta', 'MultipleObjectsReturned', 'REQUIRED_FIELDS', 'USERNAME_FIELD', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_password', '_perform_date_checks', '_perform_unique_checks', '_save_parents', '_save_table', '_set_pk_val', '_state', 'avatar', 'bio', 'birthdate', 'check', 'check_password', 'clean', 'clean_fields', 'conversation_set', 'currency', 'date_error_message', 'date_joined', 'delete', 'email', 'email_user', 'first_name', 'from_db', 'full_clean', 'gender', 'get_all_permissions', 'get_currency_display', 'get_deferred_fields', 'get_email_field_name', 'get_full_name', 'get_gender_display', 'get_group_permissions', 'get_language_display', 'get_next_by_date_joined', 'get_previous_by_date_joined', 'get_session_auth_hash', 'get_short_name', 'get_username', 'groups', 'has_module_perms', 'has_perm', 'has_perms', 'has_usable_password', 'id', 'is_active', 'is_anonymous', 'is_authenticated', 'is_staff', 'is_superuser', 'language', 'last_login', 'last_name', 'list_set', 'logentry_set', 'message_set', 'natural_key', 'normalize_username', 'objects', 'password', 'pk', 'prepare_database_save', 'refresh_from_db', 'reservation_set', 'review_set', 'room_set', 'save', 'save_base', 'serializable_value', 'set_password', 'set_unusable_password', 'superhost', 'unique_error_message', 'user_permissions', 'username', 'username_validator', 'validate_unique']

from rooms.models import Room
room1 = Room.objects.get(name="집입니다요")
print(room1)  # 집입니다요
vars(room1)  # {'_state': <django.db.models.base.ModelState object at 0x0000024844855B20>, 'id': 1, 'create': datetime.datetime(2021, 6, 7, 9, 22, 37, 89094, tzinfo=<UTC>), 'update': datetime.datetime(2021, 7, 15, 6, 42, 34, 910120, tzinfo=<UTC>), 'name': '집입니다요', 'description': '아이우에요 아에 이오구', 'country': 'KR', 'city': 'seoul', 'price': 20000, 'address': 'safaf', 'gueste': 2, 'beds': 1, 'bedrooms': 1, 'baths': 1, 'check_in': datetime.time(12, 0), 'check_out': datetime.time(12, 0), 'instant_book': False, 'host_id': 2, 'room_type_id': 1}
dir(room1)  # ['DoesNotExist', 'Meta', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks', '_save_parents', '_save_table', '_set_pk_val', '_state', 'address', 'amenities', 'baths', 'bedrooms', 'beds', 'check', 'check_in', 'check_out', 'city', 'clean', 'clean_fields', 'country', 'create', 'date_error_message', 'delete', 'description', 'facilities', 'from_db', 'full_clean', 'get_country_display', 'get_deferred_fields', 'get_next_by_create', 'get_next_by_update', 'get_previous_by_create', 'get_previous_by_update', 'gueste', 'host', 'host_id', 'house_rules', 'id', 'instant_book', 'list_set', 'name', 'objects', 'photo_set', 'pk', 'prepare_database_save', 'price', 'refresh_from_db', 'reservation_set', 'review_set', 'room_type', 'room_type_id', 'save', 'save_base', 'serializable_value', 'unique_error_message', 'update', 'validate_unique']

print(room1.photo_set.count())  2 

room1.photo_set.all()  # <QuerySet [<Photo: 사진1>, <Photo: 사진2>]>
room1.photo_set.get(caption="사진1")   # <Photo: 사진1>

# 기본적으로 Room 모델에는 photo 모델이 없다.  다만 photo 모델에 FroeignKey 로 Room 모델이 연결되어 있을뿐.
# 그럼 Django 에서 자동으로 Room 모델에 Photo 모델에 접근할수 있게 연결해준다. 기본값  photo_set 이며.. photo 모델에  related_name="변경할이름" 으로 설정해줄수 있다. 
"""

"""
print(obj.file)  # room_photos/201711230700_13180923854165_1.jpg
    print(dir(obj.file))    # 생략 
    print(obj.file.path)    # C:/GitHub/nomadcoders/airbnb-cline/uploads/room_photos/201711230700_13180923854165_1.jpg  
    print(obj.file.height)  # 654
    print(obj.file.width)   # 540
    print(obj.file.size)    # 117255
    print(obj.file.url)     # /media/room_photos/201711230700_13180923854165_1.jpg
"""