from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
import json
from app01 import models
from app01.utils.bootstarpModelForm import BootStrapModeForm
from django import forms
from django.views.decorators.csrf import csrf_exempt
from app01.utils.pagination import Pagination


class TaskModelForm(BootStrapModeForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            # "detail": forms.Textarea,
            "detail": forms.TextInput,
        }


@csrf_exempt
def task_list(request):
    """任务列表"""
    queryset = models.Task.objects.all().order_by("-id")
    page_object = Pagination(request, queryset)
    form = TaskModelForm()

    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 分页的页码
    }
    return render(request, "task_list.html", context)


def task_add(request):
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        print(2)
        return JsonResponse(data_dict)
    print(1)
    data_dict = {"status": False, "error": form.errors}  # form.errors.as_json()
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
