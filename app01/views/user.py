from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm

def user_list(request):
    """用户列表"""
    querst = models.UserInfo.objects.all()
    page_object = Pagination(request, querst, page_size=15)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()

    content = {"querst": page_queryset, "page_string":page_string}
    """
    python语法获取数据
    for obj in querst:
        print(obj.id, obj.name, obj.account, obj.create_time.strftime("%Y-%m-%d"),
            obj.gender, obj.get_gender_diaplay(), obj.depart_id, obj.depart.title)
        # obj.depart_id 获取数据库存储的值
        # obj.depart 获取数据库关联字段的对象
        # obj.depart_id.title
    """
    return render(request, "user_list.html", content)


def user_add(request):
    """用户添加"""
    if request.method == "GET":
        context = {
                "gender_choices": models.UserInfo.gender_choices,
                "depart_list": models.Department.objects.all(),
            }
        return render(request, "user_add.html", context)
    name = request.POST.get("user")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")
    account = request.POST.get("ac")
    ctime = request.POST.get("ctime")
    gender_id = request.POST.get("gd")
    depart_id = request.POST.get("dp")
    models.UserInfo.objects.create(name=name, password=pwd, age=age, account=account, 
                                   create_time=ctime, gender=gender_id, depart_id=depart_id)
    return redirect("/user/list/")


def user_model_form_add(request):
    
    """添加用户 基于modelForm"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, "user_model_form_add.html", {"form": form})

def user_edit(request, nid):
    """用户编辑"""
    # 根据id去数据库获取要编辑的那一行数据（对象）
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        form = UserModelForm(instance=row_object)     # 使用instance，将数据加入form表中
        return render(request, "user_model_form_add.html", {"form": form})
    
    form = UserModelForm(data=request.POST, instance=row_object)    # 注意，修改数据时，如果没有instance属性，默认是添加一行数据，有instance则修改覆盖该行数据
    if form.is_valid():
        form.save()
        # form.save() 默认保存的是提交的值，如果想保存自定义的值：
        #           eg: form.instance.字段名 = 值
        return redirect("/user/list/")
    return render(request, "user_model_form_add.html", {"form": form})

def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")
