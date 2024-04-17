from django.shortcuts import render
from .models import *
from datetime import datetime
def main_chart(request):
    order_by = request.GET.get("order-by")
    if order_by == 'rating':
        view_ordered_posts = Epeople.objects.order_by("-rating")[:10]
    else:
        view_ordered_posts = Epeople.objects.order_by("-views")[:10]

    context = {'posts': view_ordered_posts}
    return render(request, "chart/index.html", context)


def epeople_chart(request):
    current_month_start = datetime(datetime.now().year, datetime.now().month, 1)
    order_by = request.GET.get("order-by")
    if order_by == 'rating':
        view_ordered_posts = Epeople.objects.filter(pub_date__gte=current_month_start).order_by("-rating")[:10]
    else:
        view_ordered_posts = Epeople.objects.filter(pub_date__gte=current_month_start).order_by("-views")[:10]

    context = {'posts': view_ordered_posts}
    return render(request, "chart/charts_epeople.html", context)