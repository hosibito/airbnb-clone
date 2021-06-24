from django.db import models

from django_countries.fields import CountryField

from core import models as core_models

# from users import models as user_models


class AbstractItem(core_models.TimeStampedModel):
    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):  # 하단설명 2 참조

    """RoomType Model Definition"""

    class Meta:
        verbose_name = "Room Type"
        ordering = ["name", "create"]

    """
    Entire place, Private room, Hotel room, Shared room
    """


class Amenity(AbstractItem):

    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """Facility Model Definition"""

    class Meta:
        verbose_name = "시설"
        verbose_name_plural = "시설들"


class HouseRule(AbstractItem):

    """HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):
    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField()
    # room = models.ForeignKey(Room, on_delete=models.CASCADE) Room 정의가 밑에있어서 에러
    room = models.ForeignKey("Room", on_delete=models.CASCADE)  # 하단설명 3 참조

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()  # 하단 설명 1 참조
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    gueste = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    # host = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)  # 3 참조
    room_type = models.ForeignKey("RoomType", on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField("Amenity", blank=True)
    facilities = models.ManyToManyField(Facility, blank=True)
    house_rules = models.ManyToManyField(HouseRule, blank=True)

    def __str__(self):
        return self.name


"""   1 
    https://github.com/SmileyChris/django-countries
    나라이름을 입력할수 있게 해준다.

    pipenv install django-countries
    Add "django_countries" to INSTALLED_APPS
    from django_countries.fields import CountryField
"""

"""  2 
    Entire place, Private room, Hotel room, Shared room 등의 옵션이 올곳

    모델에 초이스를 사용해서 직접 박아넣을수도 있다. 
    어찌보면 따로 만들고 어드민에서 추가안해줘도 되니 편할수도 있다.
    다만 저건 프로그래머의 방법이다. 프로그래머가 아닌 누군가도 추가할수 있으려면
    이렇게 만드는게 낫다. 협업시에도 유리하다. 
    GENDER_MALE = "male"
        GENDER_FRMALE = "female"
        GENDER_OTHER = "other"

        GENDER_CHOICES = (
            (GENDER_MALE, "Male"),  # GENDER_MALE 은 DB에저장 Male은 form에 보여짐
            (GENDER_FRMALE, "Female"),
            (GENDER_OTHER, "Other"),
        )
"""

""" 3
 room = models.ForeignKey(Room, on_delete=models.CASCADE) 
   Room 정의가 밑에있어서 에러 따라서 
 room = models.ForeignKey("Room", on_delete=models.CASCADE) 
  "Room" 으로 string 로 바꿔주면 된다. ( model class명)
   임포트도 필요없어 지는데.. 
   https://nomadcoders.co/airbnb-clone/lectures/914 다시 볼것.

    from users import models as user_models
    host = models.ForeignKey(user_models.User, on_delete=models.CASCADE) 
    로 사용해야하나. 
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)  
    이렇게 사용가능... ( 앱이름.모델클래스명 )

"""
