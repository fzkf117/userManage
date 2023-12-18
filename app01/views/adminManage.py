from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination

def admin_list(request):
    """管理员列表"""
    # 构造搜索
    data_dict = {}
    Search_data = request.GET.get('q', "")
    if Search_data:
        data_dict["username__contains"] = Search_data
    queryset = models.Admin.objects.filter(**data_dict)
    page_object = Pagination(request, queryset)

    context = {
        'queryset': queryset,
        "page_string": page_object.html(),        # 分页的页码
        "search_data": Search_data
        }
    return render(request, 'admin_list.html', context)

from django import forms
from app01.utils.bootstarpModelForm import BootStrapModeForm
from django.core.exceptions import ValidationError
from app01.utils.encrypt import md5
class AdminModelForm(BootStrapModeForm):
    confirm_password = forms.CharField(label="确认密码", 
                                       widget=forms.PasswordInput(render_value=True)) # 密码错误不清空
    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']        # 使用model对应的字段
        widgets = {
            'password': forms.PasswordInput(render_value=True),
            }
        
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    
    def clean_confirm_password(self):
        print(self.changed_data)
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致")
        return confirm


def admin_add(request):
    """ 添加管理员 """
    context = {
        "title": "新建管理员"}
    if request.method == "GET":
        form = AdminModelForm()
        context['form'] = form
        return render(request, 'change.html', context)
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)    # {'username': '123', 'password': '123', 'confirm_password': '123'}

        form.save()
        return redirect('/admin/list/')
    context['form'] = form
    return render(request, "change.html", context)

class AdminEditModelForm(BootStrapModeForm):
    class Meta:
        model = models.Admin
        fields = ['username']


def admin_edit(request, nid):
    """"编辑管理员"""
    row_obj = models.Admin.objects.filter(id=nid).first()
    if not row_obj:
        return render(request, "404.html")
    
    context = {
        "title": "编辑管理员"}
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_obj)
        context["form"] = form
        return render(request, "change.html", context)
    form = AdminEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, "change.html", context)

def admin_delete(request, nid):
    """删除管理员"""
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')

class AdminResetModelForm(BootStrapModeForm):
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput(render_value=True)) # 密码错误不清空
    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']        # 使用model对应的字段
        widgets = {
            'password': forms.PasswordInput(render_value=True),
            }
        
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能与之前的一致")
        return md5(pwd)

    
    def clean_confirm_password(self):
        print(self.changed_data)
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致")
        return confirm


    
def admin_reset(request, nid):
    """重置密码"""
    row_obj = models.Admin.objects.filter(id=nid).first()
    if not row_obj:
        return render(request, "404.html")
    
    context = {
        "title": "重置密码 - {}".format(row_obj.username)}
    if request.method == "GET":
        form = AdminResetModelForm()
        context["form"] = form
        return render(request, "change.html", context)
    form = AdminResetModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        # print(form.cleaned_data)    # {'username': '123', 'password': '123', 'confirm_password': '123'}
        form.save()
        return redirect('/admin/list/')
    context['form'] = form
    return render(request, "change.html", context)