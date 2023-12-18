from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    """ 数据统计 """
    return render(request, "chart_list.html")


def chart_bar(request):
    """构造图书数据"""
    legend = ['销量', '业绩']
    xAxis = ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
    series = [
        {
            "name": '销量',
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": '业绩',
            "type": 'bar',
            "data": [45, 20, 46, 30, 5, 10]
        }
    ]
    result = {
        "status": True,
        "data": {
            "legend": legend,
            "xAxis": xAxis,
            "series": series
        }
    }
    return JsonResponse(result)


def hightChart_list(request):
    return render(request, "hightChart_list.html")
