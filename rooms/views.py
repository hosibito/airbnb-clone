# from datetime import datetime
from django.shortcuts import render

from . import models


def all_rooms(request):
    # print(vars(request))
    # print(dir(request))
    # now = datetime.now()
    # hungry = True
    # return render(request, "all_rooms.html", context={"now": now, "hungry": hungry})
    all_rooms = models.Room.objects.all()    
    return render(request, "rooms/home.html", context={"rooms": all_rooms})
