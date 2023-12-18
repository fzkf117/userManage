from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination

def depart_list(request):
    """部门表"""
    querst = models.Department.objects.all()
    page_object = Pagination(request, queryset=querst, page_size=15)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()

    content = {"querst": page_queryset, "page_string":page_string}
    return render(request, "depart_list.html", content)

def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request, 'depart_add.html')
    title = request.POST.get("title")
    models.Department.objects.create(title=title)
    return redirect("/depart/list/")

def depart_delete(reauest):
    """删除部门"""
    nid = reauest.GET.get("nid")
    models.Department.objects.filter(id=int(nid)).delete()
    return redirect("/depart/list/")

def depart_edit(request, nid):
    """编辑部门"""
    if request.method == "GET":
        row_obj = models.Department.objects.filter(id=nid).first()
        return render(request, "depart_edit.html", {"row_obj": row_obj})
    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")
