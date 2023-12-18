from django.db import models
import ssl


# Create your models here.

class Admin(models.Model):
    """管理员"""
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username


class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name='标题', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账号余额', max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name='入职时间')
    create_time = models.DateField(verbose_name='入职时间')

    """
    下面将UserInfo创建部门字段, 与部门表进行关联
        --字段关联使用方法
            -方法: models.ForeignKey()
            -关键字: to: 与某张表关联
            -关键字: to_field: 与表中的某个字段进行关联
        --注意: 该字段使用关联后, 该字段的命名自动增加"_id"", 例如: depart 生成后表 depart_id
    """

    depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    """
    使用关联表时, 注意事项: 
        1. 关联表目的: 节省存储开销
        2. 有数据关联时, 什么时候却不使用关联表: 查询次数过于频繁, 为了实现快速查找,  允许数据冗余
        3. 使用关联表时, 关联字段的数据必须是已经存在的, 使用方法models.ForeignKey(to="", to_Field="")
        4. 当关联字段 对应的 被关联字段被删除, 关键字on_delete: 
            --(1)级联删除, 也就是关联所在的行数据也会被删, 方法:  models.ForeignKey(to="", to_Field="", on_delete=models.CASCADE)
            --(2)字段置空, 也就是关联字段变空, 方法: models.ForeignKey(to="", to_Field="", null=True, black=True, on_delete=models.SET_NULL)
    """

    gender_choices = (
        (1, "男"),
        (2, "女")
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)
    """
    对很少行数据, 不会常改的数据表, 不需要再建一张表进行关联
        -- 可以先定义好结构(元组), 使用choices来限制输入的数据
    """


class PrettyNum(models.Model):
    """靓号管理"""
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    # 想要允许为空 使用属性null=True, blank=True
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2, default=0)

    level_choice = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choice, default=1)

    status_choies = (
        (1, "已使用"),
        (2, "未使用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choies, default=2)


class Task(models.Model):
    """任务"""
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时")
    )

    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=3)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详细信息")
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)


class Order(models.Model):
    """ 工单 """
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choices = (
        (1, "待支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    admin = models.ForeignKey(verbose_name="管理员", to='Admin', on_delete=models.CASCADE)


class Boss(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    img = models.CharField(verbose_name="头像", max_length=32)



class City(models.Model):
    name = models.CharField(verbose_name="名称", max_length=32)
    count = models.IntegerField(verbose_name="人口")
    img = models.FileField(verbose_name="login", max_length=32, upload_to="city/")     # 数据库中实际也是CharField，不用手动上传文件，upload_toc参数会将文件保存到media文件夹
