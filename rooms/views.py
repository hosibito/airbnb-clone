from django.utils import timezone
from django.views.generic import ListView, DetailView

from django.shortcuts import render

from . import models
from . import forms


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 4
    ordering = "-create"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['time_now'] = now

        return context

        # print(context)
        # print(dir(context))
        # print(dir(context["page_obj"]))


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


def search(request):
    country = request.GET.get("country")

    if country:
        form = forms.SearchForm(request.GET)
        # 입력된 정보를 기억한다. bounded form 이 되어 데이터 무결성 검사를 하게된다.

        if form.is_valid():  # 폼 데이터가 무결성인지 알려준다.
            print(form.cleaned_data)
            # {'city': 'Anywhere', 'country': 'KR', ...
            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guests")
            bedrooms = form.cleaned_data.get("bedrooms")
            beds = form.cleaned_data.get("beds")
            baths = form.cleaned_data.get("baths")
            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")
            houserules = form.cleaned_data.get("houserules")

            filter_args = {}

            if city != "Anywhere":
                filter_args["city__startswith"] = city

            filter_args["country"] = country

            if room_type is not None:
                filter_args["room_type"] = room_type

            if price is not None:
                filter_args["price__lte"] = price

            if guests is not None:
                filter_args["guests__gte"] = guests

            if bedrooms is not None:
                filter_args["bedrooms__gte"] = bedrooms

            if beds is not None:
                filter_args["beds__gte"] = beds

            if baths is not None:
                filter_args["baths__gte"] = baths

            if instant_book is True:
                filter_args["instant_book"] = True

            if superhost is True:
                filter_args["host__superhost"] = True

            for s_ame in amenities:
                filter_args["amenities"] = s_ame

            for s_facil in facilities:
                filter_args["facilities"] = s_facil

            for s_h_rule in houserules:
                filter_args["house_rules"] = s_h_rule

            print(filter_args)

            rooms = models.Room.objects.filter(**filter_args)
    else:
        form = forms.SearchForm()   # unbounded form

    return render(request, "rooms/search.html", {"form": form, "rooms": rooms})


"""
=== 함수형 serch 구현 
def search(request):
    country = request.GET.get("country")

    if country:
        form = forms.SearchForm(request.GET)
        # 입력된 정보를 기억한다. bounded form 이 되어 데이터 무결성 검사를 하게된다.

        if form.is_valid():  # 폼 데이터가 무결성인지 알려준다.
            print(form.cleaned_data)
            # {'city': 'Anywhere', 'country': 'KR', ...
            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guests")
            bedrooms = form.cleaned_data.get("bedrooms")
            beds = form.cleaned_data.get("beds")
            baths = form.cleaned_data.get("baths")
            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")
            houserules = form.cleaned_data.get("houserules")

            filter_args = {}

            if city != "Anywhere":
                filter_args["city__startswith"] = city

            filter_args["country"] = country

            if room_type is not None:
                filter_args["room_type"] = room_type

            if price is not None:
                filter_args["price__lte"] = price

            if guests is not None:
                filter_args["guests__gte"] = guests

            if bedrooms is not None:
                filter_args["bedrooms__gte"] = bedrooms

            if beds is not None:
                filter_args["beds__gte"] = beds

            if baths is not None:
                filter_args["baths__gte"] = baths

            if instant_book is True:
                filter_args["instant_book"] = True

            if superhost is True:
                filter_args["host__superhost"] = True

            for s_ame in amenities:
                filter_args["amenities"] = s_ame

            for s_facil in facilities:
                filter_args["facilities"] = s_facil

            for s_h_rule in houserules:
                filter_args["house_rules"] = s_h_rule

            print(filter_args)

            rooms = models.Room.objects.filter(**filter_args)
    else:
        form = forms.SearchForm()   # unbounded form

    return render(request, "rooms/search.html", {"form": form, "rooms": rooms})

=====#13 SEARCHVIEW - serch를 Django forms를 -이용해서 구현 입력값 저장하는법!=============
def search(request):

    country = request.GET.get("country")

    if country:
        form = forms.SearchForm(request.GET)
        # 입력된 정보를 기억한다. bounded form 이 되어 데이터 무결성 검사를 하게된다.
        if form.is_valid():  # 폼 데이터가 무결성인지 알려준다.
            print(form.cleaned_data)
            # {'city': 'Anywhere', 'country': 'KR', 'room_type': <RoomType: Hotel room>,
            # 'price': 200, 'guests': None, 'bedrooms': None, 'beds': None,
            # 'baths': None, 'instant_book': False, 'superhost': False,
            # 'amenities':
            # <QuerySet [<Amenity: 샤워>, <Amenity: Wi-Fi>, <Amenity: Washer>]>,
            # 'facilities': <QuerySet []>, 'houserules': <QuerySet []>}

    else:
        form = forms.SearchForm()   # unbounded form

    return render(request, "rooms/search.html", {"form": form})


======note # 13 serch를 장고 도움없이 쌩으로 구현 3 1=============
def search(request):
    # form
    # print(countries)  # <django_countries.Countries object at 0x00000194E4EEE940>
    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()
    house_rules = models.HouseRule.objects.all()

    # choices
    city = str.capitalize(request.GET.get("city", "Anywhere"))
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))  # 그냥두면 on / False 이므로
    superhost = bool(request.GET.get("superhost", False))
    # print(instant, super_host)  # False on
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")
    s_house_rules = request.GET.getlist("house_rules")
    # print(s_amenities, s_facilities, s_house_rules)
    # ['3', '7', '11'] ['3', '4'] ['1']

    form = {
        "city": city,
        "s_country": country,
        "s_room_type": room_type,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "instant": instant,
        "superhost": superhost,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "s_house_rules": s_house_rules,
    }

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
        "house_rules": house_rules,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    if superhost is True:
        filter_args["host__superhost"] = True

    # print(s_amenities)  # ['1', '2', '3']
    if len(s_amenities) > 0:
        for s_ame in s_amenities:
            filter_args["amenities__pk"] = int(s_ame)

    if len(s_facilities) > 0:
        for s_facil in s_facilities:
            filter_args["facilities__pk"] = int(s_facil)

    if len(s_house_rules) > 0:
        for s_h_rule in s_house_rules:
            filter_args["house_rules__pk"] = int(s_h_rule)

    # print(filter_args)

    rooms = models.Room.objects.filter(**filter_args)

    print(rooms)

    return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})


    --- 비추천 방법 ----
    qs = models.Room.objects.filter().filter().filter()

    if price != 0:
        qs = qs.filter(price__lte=price)

    if bedrooms != 0:
        qs = qs.filter(price__lte=bedrooms)

    ---추천 방법---
    filter_args = {}

    if price != 0:
        filter_args["price__lte"] = price

    print(filter_args)  # {'price__lte': 30}

    rooms = models.Room.objects.filter(**filter_args)

    print(rooms)
    # <QuerySet [<Room: Piece magazine leave nature.>,
    # <Room: Conference behind key small base TV.>]>
"""

""" note # 12 함수형 detailvoew(404관련포함)
from django.http import Http404
from django.shortcuts import render

def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:
        raise Http404()
"""

""" note # 11 페이지3 클래스형
from django.views.generic import ListView
from . import models

class HomeView(ListView):
    model = models.Room
    paginate_by = 10
    paginate_orphans = 4
    ordering = "-create"
    # page_kwarg = 'page' # 기본값으로 들어가있다.

    # 1 자동으로 room_list.html 파일에 연결하려한다.
    # (바꿀수 있다.template_name = None  template_name_suffix = '_list' )
    # 템플릿에는 object_list 와 page_obj 가 자동 전달된다. ( 바꿀수 있다. context_object_name = None )

class HomeView(ListView):
    model = models.Room
    paginate_by = 10
    paginate_orphans = 4
    ordering = "-create"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['time_now'] = now
        print(context)
        print(dir(context))
        print(dir(context["page_obj"]))
        return context
"""

""" note # 11 페이지2 함수형
from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, Paginator

def all_rooms(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()  # 장고 쿼리는 게으르다.. 실제로 정보를 조회할때 처리된다.
    paginator = Paginator(room_list, 10, orphans=4)

    try:
        page_rooms = paginator.page(int(page))
        return render(request, "rooms/home.html", {"page_rooms": page_rooms})
    except EmptyPage:
        return redirect("/")

def all_rooms(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()  # 장고 쿼리는 게으르다.. 실제로 정보를 조회할때 처리된다.
    paginator = Paginator(room_list, 10)
    rooms = paginator.get_page(page)
    print(vars(rooms))
    print(dir(rooms))
    print(vars(rooms.paginator))
    print(dir(rooms.paginator)
    print(rooms.paginator)
    # <django.core.paginator.Paginator object at 0x000002AB93348430>
    print(rooms)  # <Page 1 of 12>

    return render(request, "rooms/home.html", context={"rooms": rooms})

def all_rooms(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()  # 장고 쿼리는 게으르다.. 실제로 정보를 조회할때 처리된다.
    paginator = Paginator(room_list, 10, orphans=4)
    # orphans=4 : 맨 마지막페이지의 object가 4개보다 작다면 그전페이지에 추가해서 보인다.
    # ex) 마지막 페이지에 3 개라면.. 마지막 페이지를 없애고 그전페이지에 13개를 보여준다.
    page_rooms = paginator.get_page(page)
    # Page범위를 벗어나거나 잘못된 페이지 번호를 처리하면서 지정된 1부터 시작하는 인덱스가 있는 개체를 반환.
    # 페이지가 숫자가 아니면 첫 번째 페이지를 반환, 음수이거나 페이지 수보다 크면 마지막 페이지를 반환
    try:
        page_rooms = paginator.page(int(page))
    except EmptyPage:
        page_rooms = paginator.page(1)

    return render(request, "rooms/home.html", context={"page_rooms": page_rooms})
"""

""" note # 11 페이지1(100%수동)
    # print(request.GET)
    # # http://127.0.0.1:8000/?page=1 일때 <QueryDict: {'page': ['1']}>
    # print(request.GET.get("page"))  # 1
    # all_rooms = models.Room.objects.all()[1:10]

def all_rooms(request):
    page = request.GET.get("page", 1)
    page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)  # 올림

    return render(request, "rooms/home.html", context={
        "rooms": all_rooms,
        "page": page,
        "page_count": page_count,
        "page_range": range(1, page_count + 1),
    })

"""

""" note # 10 참조
def all_rooms(request):
    # print(vars(request))
    # print(dir(request))
    # now = datetime.now()
    # hungry = True
    # return render(request, "all_rooms.html", context={"now": now, "hungry": hungry})
    all_rooms = models.Room.objects.all()
    return render(request, "rooms/home.html", context={"rooms": all_rooms})
"""
