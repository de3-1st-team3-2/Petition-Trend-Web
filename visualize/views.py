from django.shortcuts import render
from .models import *


def main_chart(request):
    order_by = request.GET.get("order-by")
    if order_by == 'rating':
        view_ordered_posts = Epeople.objects.order_by("-rating")[:10]
    else:
        view_ordered_posts = Epeople.objects.order_by("-views")[:10]

    context = {'posts': view_ordered_posts}
    return render(request, "chart/index.html", context)


def epeople_chart(request):
    order_by = request.GET.get("order-by")
    if order_by == 'rating':
        view_ordered_posts = Epeople.objects.order_by("-rating")[:10]
    else:
        view_ordered_posts = Epeople.objects.order_by("-views")[:10]

    context = {'posts': view_ordered_posts}
    return render(request, "chart/charts.html", context)

def cw24_chart(request):
    view_ordered_posts = CW24.objects.order_by("-views")[:10]

    context = {'posts': view_ordered_posts}
    return render(request, "chart/cw24_charts.html", context)
    