from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class authLogin(MiddlewareMixin):
    """中间件
    返回值: None-> 继续往下一个中间件走
            HttpsResponse, render, redirect 与视图函数返回一样
    """

    def process_request(self, request):
        if request.path_info in ["/login/", "/image/code/", '/order_list/']:
            return
        info_dict = request.session.get("info")
        # print(info_dict)
        if info_dict:
            return
        return redirect("/login/")

    def process_response(self, request, response):
        return response
