import os.path

from django.shortcuts import render, HttpResponse, redirect

from django import forms
from app01.utils.bootstarpModelForm import BootStrapForm, BootStrapModeForm
from app01 import models
from django.conf import settings


class UpForm(BootStrapForm):
    BootStrap_exclude_fields = ["img"]
    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")


def upload_list(request):
    """form"""
    title = "form 上传"
    if request.method == "GET":
        form = UpForm()
        return render(request, "upload_list.html", context={"form": form, "title": title})
    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        print(form.cleaned_data)
        # {'name': '123', 'age': 22, 'img': <InMemoryUploadedFile: 4ccda31e1356c9c1af2d70ddd07f30d.jpg (image/jpeg)>}
        # 将文件路径写入数据库
        image = form.cleaned_data.get("img")
        file_path = os.path.join(settings.MEDIA_ROOT, image.name)
        with open(file_path, mode="wb") as file:
            for chunk in image.chunks():
                file.write(chunk)
        models.Boss.objects.create(
            name=form.cleaned_data["name"],
            age=form.cleaned_data["age"],
            img=file_path
        )
        return HttpResponse("...")
    return render(request, "upload_list.html", context={"form": form, "title": title})


class UploadModelForm(BootStrapModeForm):
    BootStrap_exclude_fields = ["img"]

    class Meta:
        model = models.City
        fields = "__all__"


def upload_model_form(request):
    """上传文件和数据（ModelForm）"""
    title = "ModelForm文件上传"
    if request.method == "GET":
        form = UploadModelForm()
        return render(request, "upload_list.html", {"form": form, "title": title})
    form = UploadModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/city/list/")
    return render(request, "upload_list.html", {"form": form, "title": title})

