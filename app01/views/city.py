from django.shortcuts import render
from app01 import models

def city_list(request):
    queryset = models.City.objects.all()
    return render(request, "city_list.html", {"queryset": queryset})
    pass