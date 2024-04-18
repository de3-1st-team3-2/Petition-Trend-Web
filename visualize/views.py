from django.shortcuts import render
from .models import *
from datetime import datetime

def main_index(request):
    return render(request, "chart/index.html")


def epeople_chart(request):
    current_month_start = datetime(datetime.now().year, datetime.now().month, 1)
    order_by = request.GET.get("order-by")
    if order_by == 'rating':
        view_ordered_posts = Epeople.objects.filter(pub_date__gte=current_month_start).order_by("-rating")[:10]
    else:
        view_ordered_posts = Epeople.objects.filter(pub_date__gte=current_month_start).order_by("-views")[:10]

    context = {'posts': view_ordered_posts}
    return render(request, "chart/charts_epeople.html", context)

def congress_chart(request):
    order_by = request.GET.get("order-by")
    view_ordered_posts = Congress.objects.order_by("-rating")[:10]

    context = {'posts': view_ordered_posts}
    return render(request, "chart/charts_congress.html", context)


def cw24_chart(request):
    view_ordered_posts = CW24.objects.order_by("-views")[:10]

    context = {'posts': view_ordered_posts}
    return render(request, "chart/charts_cw24.html", context)

def ideaseoul_chart(request):
    order_by = request.GET.get("order-by")
    view_ordered_posts = Ideaseoul.objects.order_by("-views")[:10]

    context = {'posts': view_ordered_posts}
    return render(request, "chart/charts_ideaseoul.html", context)

def subthink_chart(request):
    participants_ordered_posts = SubThink.objects.order_by("-participants")[:10]

    context = {'posts': participants_ordered_posts}
    return render(request, "chart/charts_subthink.html", context)