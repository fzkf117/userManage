from django import forms

class BootStrap:
    BootStrap_exclude_fields = []

    # 执行父类 重写（给对象添加属性）
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 循环拿到所有对象，从而拿到对象的插件widget， 为对象的input添加属性
        for name, field in self.fields.items():
            if name in self.BootStrap_exclude_fields:
                continue
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {"class": "form-control", "placeholder": field.label}

class BootStrapModeForm(BootStrap, forms.ModelForm):
    pass


class BootStrapForm(BootStrap, forms.Form):
    pass