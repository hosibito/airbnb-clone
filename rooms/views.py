from django.utils import timezone
from django.views.generic import ListView

from . import models


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
