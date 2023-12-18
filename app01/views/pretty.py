from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import PrettyModelForm, PrettyEditModelForm

def pretty_list(request):
    """靓号管理"""
    # todo 加入搜索功能

    data_dict = {}
    Search_data = request.GET.get('q', "")
    if Search_data:
        data_dict["mobile__contains"] = Search_data
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request, queryset, page_size=15)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()

    content = {"queryset": page_queryset, "search_data": Search_data, "page_string":page_string}

    return render(request, "pretty_list.html", content)
    
def pretty_add(request):
    """号码添加"""
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_add.html", {"form": form})

def pretty_edit(request, nid):
    """号码信息修改""" 
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, "pretty_edit.html", {"form": form})
    form = PrettyEditModelForm(instance=row_object, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_edit.html", {"form": form})

def pretty_delete(request, nid):
    """删除靓号"""
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")