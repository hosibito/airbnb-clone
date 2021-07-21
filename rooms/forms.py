from django import forms

from django_countries.fields import CountryField

from . import models


class SearchForm(forms.Form):
    # city = forms.CharField(initial="Anywhere", widget=forms.Textarea)
    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()  # django_countries 깃허브 문서에 있슴.
    room_type = forms.ModelChoiceField(
        required=False,
        empty_label="Any kinds",
        queryset=models.RoomType.objects.all(),
    )
    price = forms.IntegerField(required=False, min_value=1,)
    guests = forms.IntegerField(required=False, min_value=1, max_value=10)
    bedrooms = forms.IntegerField(required=False, min_value=1,)
    beds = forms.IntegerField(required=False, min_value=1,)
    baths = forms.IntegerField(required=False, min_value=1,)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    houserules = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.HouseRule.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


""" 노트 # 13 serch를 Django forms를 이용해서 구현 참고

    widget 으로 다른 위젯으로 바꿔줄수 있따. 각 필드에 맞는 기본 위젯이 정의되어이싿.

    empty_lable   입력이 안되어있을때 기본 valve값을 넣어준다.
    default = 값과 비교해서 볼것..

    여러 옵션들이 있으니 장고 공식문서를 참고해볼것.


    https://docs.djangoproject.com/ko/3.2/ref/forms/widgets/

"""
