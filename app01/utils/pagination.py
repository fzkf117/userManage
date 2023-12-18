"""
自定义bootstrap分页组件

使用：
    1.view.py:
        def info_list(request):
            # 获取全部的数据->list
            queryset = models.PreattyNum.objects.all()

            # 实例化分页组件
            page_object = Pagination(request, queryset)

            # 返回参数给html
            content = {
                "queryset": page_object.page_queryset,  # 分完页的数据
                "page_string": page_object.html()        # 分页的页码
            }

            renturn render(request, "prety_list.html", context)

    2.html
        数据：
            {% for obj in queryset %}
                {{obj.xx}}
            {% endfor %}

        分页：
            <ul class="pageination">
                {{ page_string }}
            </ul>

            或
                <div class="container" style="margin: 0 auto; display: flex; justify-content: center; align-items: center;">
                    <ul class="pagination">
                        {{page_string}}
                    </ul>
                </div>

"""
from django.utils.safestring import mark_safe
import copy


class Pagination(object):
    def __init__(self, request, queryset, page_parame="page", page_size=10, plus=5) -> None:
        """
        :param request: 请求对象
        :param queryset: 符合条件的数据（根据这个条件进行分页处理）
        :param page_parame: 在url中传递获取分页的参数
        :param page_size: 每页显示多少条数据
        :param plus: 显示当前或后续的第几页

        """
        query_object = copy.deepcopy(request.GET)
        query_object._mutable = True  # 关键修改
        self.query_object = query_object

        page = request.GET.get(page_parame, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_parame = page_parame
        self.page_size = page_size
        if page == 0:
            page = 1
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start: self.end]
        total_count = queryset.count()
        tatal_page_count, div = divmod(total_count, page_size)
        if div:
            tatal_page_count += 1
        self.tatal_page_count = tatal_page_count
        self.plus = plus

    def html(self):
        # 显示当前的前5页，后5页

        if self.tatal_page_count <= 2 * self.plus + 1:  # 少于11页

            start_page = 1
            end_page = self.tatal_page_count
        else:  # 多于11页
            if self.page <= self.plus:  # 当前页小于极小值
                start_page = 1
                end_page = 2 * self.plus + 1
            else:  # 当前页大于极小值
                if (self.page + self.plus) > self.tatal_page_count:  # 当前页大于总页数
                    start_page = self.tatal_page_count - 2 * self.plus
                    end_page = self.tatal_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []

        # 首页
        if self.page != 1:
            self.query_object.setlist(self.page_parame, [1])
            page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_object.urlencode()))
        else:
            page_str_list.append('<li class="previous disabled"><a>首页</a></li>')

        # 上一页
        if self.page > 1:
            self.query_object.setlist(self.page_parame, [self.page - 1])
            prev = '<li><a href="?{}">上一页</li>'.format(self.query_object.urlencode())
        else:
            prev = '<li  class="previous disabled"><a>上一页</li>'
        page_str_list.append(prev)

        # 页面
        for i in range(start_page, end_page + 1):
            if i == self.page:
                self.query_object.setlist(self.page_parame, [i])
                ele = '<li class="active"><a href="?{}">{}</li>'.format(self.query_object.urlencode(), i)
            else:
                self.query_object.setlist(self.page_parame, [i])
                ele = '<li><a href="?{}">{}</li>'.format(self.query_object.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.tatal_page_count:
            self.query_object.setlist(self.page_parame, [self.page + 1])
            prev = '<li><a href="?{}">下一页</li>'.format(self.query_object.urlencode())
        else:
            prev = '<li  class="previous disabled"><a>下一页</li>'
        page_str_list.append(prev)

        # 尾页
        if self.page != self.tatal_page_count:
            if self.page > self.tatal_page_count:
                page_str_list.append('<li class="previous disabled"><a>尾页</a></li>')
            else:
                self.query_object.setlist(self.page_parame, [self.tatal_page_count])
                page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_object.urlencode()))
        else:
            page_str_list.append('<li class="previous disabled"><a>尾页</a></li>')

        # 总页
        page_str_list.append('<li class="previous disabled"><a>共{}页</a></li>'.format(self.tatal_page_count))

        # 手动跳转 
        search_string = """
            <li>
            <form action="" style="float: left; margin-left:-1px;">
                <div class="input-group" >
                    <input type="number" name="{}" class="form-control" placeholder="页码" min="1" step="1" style="width:100px">
                    <span class="input-group-btn">
                        <button class="btn btn-primary" type="submit">跳转</button>
                    </span>
                </div>
            </form>
            </li>
        """.format(self.page_parame)

        #         search_string = """
        #             <li>
        # <form style="float: left;margin-left:0px">
        #     <input type="text" name="page" class="form-control" placeholder="页码" style="position: relative; display: inline-block; width: 80px; border-radius: 0;" >
        #     <button style="border-radius: 1; margin-left:-5px" class="btn btn-primary" type="submit">跳转</button>
        # </form>
        #             </li>
        #         """.format(self.page_parame)

        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string
