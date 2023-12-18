from app01 import models
from app01.utils.bootstarpModelForm import BootStrapModeForm
from django import forms
from django.core.validators import RegexValidator       # django使用正则
from django.core.exceptions import ValidationError      # django异常返回

class UserModelForm(BootStrapModeForm):
    name = forms.CharField(min_length=3, label="姓名")
    class Meta:
        model = models.UserInfo
        fields =  ["name", "password", "age", "account", "create_time", "depart", "gender"]        # 使用model对应的字段
        """        widgets = {                                                   # 添加属性插件， 缺点：要重复写
                    "name": forms.TextInput(attrs={"class": "form-control"})     # form表单创建的name的input, 没有属性，在这给它添加属性
                    "password": forms.PasswordInput(attrs={"class": "form-control"})
                    "age": forms.PasswordInput(attrs={"class": "form-control"})
                }
        """


class PrettyModelForm(BootStrapModeForm):
    # 手机验证方式1：
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r"(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-79])|(?:5[0-35-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9[189]))\d{8}", "手机号码格式不正确")]
        )
    
    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # fields = "__all__"        # 全部
        # exclude = ["level"]         # 排除
    


    # 字段验证方法（钩子）2：
    def clean_mobile(self):     # 固定命名写法：clear_字段名
        text_mobile = self.cleaned_data["mobile"]   # 获取要验证的值：self.cleaned_data["字段名"]
        # 进行校验
        exists = models.PrettyNum.objects.filter(mobile=text_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        if len(text_mobile) != 11:
            raise ValidationError("长度不符合")
        # print(re.mat(r"(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-79])|(?:5[0-35-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9[189]))\d{8}", "手机号码格式不正确"))
        return text_mobile
    

class PrettyEditModelForm(BootStrapModeForm):
    # mobile = forms.CharField(disabled=True, label="手机号")   # 设置手机号不可修改
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r"(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-79])|(?:5[0-35-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9[189]))\d{8}", "手机号码格式不正确")]
    )
    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]


    def clean_mobile(self):     # 固定命名写法：clean_字段名
        text_mobile = self.cleaned_data["mobile"]   # 获取要验证的值：self.cleaned_data["字段名"]
        # 进行校验
        # 先排除自己 self.instance.pk 是操作的id
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=text_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        if len(text_mobile) != 11:
            raise ValidationError("长度不符合")
        # print(re.mat(r"(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-79])|(?:5[0-35-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9[189]))\d{8}", "手机号码格式不正确"))
        return text_mobile