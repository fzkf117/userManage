"""userManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, re_path
from app01.views import depart, pretty, user, adminManage, account, task, order, chart, upload, city
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}, name="media"),

    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/delete/', depart.depart_delete),
    path('depart/<int:nid>/edit/', depart.depart_edit),

    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/model/form/add/', user.user_model_form_add),
    path('user/<int:nid>/edit/', user.user_edit),
    path('user/<int:nid>/delete/', user.user_delete),

    # 靓号管理
    path('pretty/list/', pretty.pretty_list),
    path('pretty/add/', pretty.pretty_add),
    path('pretty/<int:nid>/edit/', pretty.pretty_edit),
    path('pretty/<int:nid>/delete/', pretty.pretty_delete),

    # 管理员的管理
    path('admin/list/', adminManage.admin_list),
    path('admin/add/', adminManage.admin_add),
    path('admin/<int:nid>/edit/', adminManage.admin_edit),
    path('admin/<int:nid>/delete/', adminManage.admin_delete),
    path('admin/<int:nid>/reset/', adminManage.admin_reset),

    # 登录
    path('login/', account.login),
    path('', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),

    # 
    path('task/list/', task.task_list),
    path('task/add/', task.task_add),

    # 订单管理
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),
    path('order/detail/', order.order_detail),
    path('order/edit/', order.order_edit),

    # 数据统计
    path('eChart/list/', chart.chart_list),
    path('Chart/bar/', chart.chart_bar),
    path('hightChart/list/', chart.hightChart_list),


    # 文件信息上传
    path('upload/list/', upload.upload_list),
    path('upload/modelForm/', upload.upload_model_form),

    # 城市列表
    path('city/list/', city.city_list),


]
