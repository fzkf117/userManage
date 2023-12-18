from django.shortcuts import render, HttpResponse, redirect

from django import forms
from app01.utils.bootstarpModelForm import BootStrapForm
from app01.utils.encrypt import md5
from app01 import models
from app01.utils.code import check_code
from io import BytesIO


class LoginForm(BootStrapForm):
    username = forms.CharField(label="用户名", 
                               widget=forms.TextInput, 
                               required=True,       # 必填，不能为空
                               )
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True), required=True)

    code = forms.CharField(label="验证码", widget=forms.TextInput)

    def clean_password(self):   # 钩子方法，回调
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

def login(request):
    """登录"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功, 获取
        print(form.cleaned_data)

        # 验证码校验
        user_input_cdoe = form.cleaned_data.pop("code")
        code = request.session.get("image_code", "")
        if code.upper() != user_input_cdoe.upper():
            form.add_error("code", "验证码错误 ")
            return render(request, "login.html", {'form': form})

        # 去数据库校验用户的用户名和密码是否成功, 获取用户对象
        # admin_obj = models.Admin.objects.filter(username="xxx", password="xxx").first()
        admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_obj:
            form.add_error("password", "用户名或密码错误")
            request.session.pop("image_code")       
            return render(request, "login.html", {'form': form})

        # 用户名或密码正确
        # 生成随机字符串，写到浏览器的cookie中， 写入session中
        request.session["info"] = {"id": admin_obj.id, "name":  admin_obj.username}
        request.session.set_expiry(60 * 60 *24)
        request.session.pop("image_code")
        return redirect("/admin/list/")
    return render(request, "login.html", {'form': form})


def logout(request):
    """注销"""
    request.session.clear()
    return redirect("/login/")

def image_code(request):
    img, code_string = check_code()

    # 写入session中，以便后续进行校验
    request.session["image_code"] = code_string
    # 设置60秒超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, "png")
    return HttpResponse(stream.getvalue())