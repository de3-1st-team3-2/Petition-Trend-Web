from django.shortcuts import render
from .models import *
from datetime import datetime, timedelta

def main_index(request):
    return render(request, "chart/index.html")


def epeople_chart(request):
    current_month_start = datetime(datetime.now().year, datetime.now().month, 1)
    order_by = request.GET.get("order-by")
    if order_by == 'rating':
        view_ordered_posts = Epeople.objects.filter(pub_date__gte=current_month_start).order_by("-rating")[:10]
    else:
        view_ordered_posts = Epeople.objects.filter(pub_date__gte=current_month_start).order_by("-views")[:10]

    columns = ['제목', '처리기관', '분야', '작성일', '처리상태', '조회수', '별점']
    view_ordered_posts_lst = []

    for elem in view_ordered_posts:
        result_lst = []
        result_lst.append((elem.title, elem.url))
        result_lst.append(elem.agency)
        result_lst.append(elem.field)
        result_lst.append(elem.pub_date.strftime("%Y-%m-%d"))
        result_lst.append(elem.status)
        result_lst.append(elem.views)
        result_lst.append(elem.rating)
        view_ordered_posts_lst.append(result_lst)

    context = {'columns' : columns, 'posts': view_ordered_posts_lst, 'site_name': '국민 신문고'}
    return render(request, "chart/uniform_charts.html", context)

def congress_chart(request):
    order_by = request.GET.get("order-by")
    view_ordered_posts = Congress.objects.order_by("-rating")[:10]

    columns = ['제목', '처리기관', '분야', '작성일', '처리상태', '동의수']
    view_ordered_posts_lst = []

    for elem in view_ordered_posts:
        result_lst = []
        result_lst.append((elem.title, elem.url))
        result_lst.append(elem.agency)
        result_lst.append(elem.category)
        result_lst.append(elem.pub_date.strftime("%Y-%m-%d"))
        result_lst.append(elem.status)
        result_lst.append(elem.rating)
        view_ordered_posts_lst.append(result_lst)
        
    context = {'columns' : columns, 'posts': view_ordered_posts_lst, 'site_name': '국회 국민 동의 청원'}
    return render(request, "chart/uniform_charts.html", context)


def cw24_chart(request):
    view_ordered_posts = CW24.objects.order_by("-views")[:10]

    columns = ['제목', '처리기관', '추진상황', '작성일', '기간', '조회수', '댓글수']
    view_ordered_posts_lst = []

    for elem in view_ordered_posts:
        result_lst = []
        result_lst.append((elem.title, elem.url))
        result_lst.append(elem.agency)
        result_lst.append(elem.status)
        result_lst.append(elem.pub_date.strftime("%Y-%m-%d"))
        
        start_date_str = elem.start_date.strftime("%Y-%m-%d")
        end_date_str = elem.end_date.strftime("%Y-%m-%d")
        result_lst.append(f"{start_date_str} ~ {end_date_str}")
        result_lst.append(elem.views)
        result_lst.append(elem.comment_num)
        view_ordered_posts_lst.append(result_lst)
        
    context = {'columns' : columns, 'posts': view_ordered_posts_lst, 'site_name': '청원 24'}
    return render(request, "chart/uniform_charts.html", context)

def ideaseoul_chart(request):
    order_by = request.GET.get("order-by")
    view_ordered_posts = Ideaseoul.objects.order_by("-views")[:10]

    columns = ['제목', '분야', '작성일', '기간', '처리상태', '조회수']
    view_ordered_posts_lst = []

    for elem in view_ordered_posts:
        result_lst = []
        result_lst.append((elem.title, elem.url))
        result_lst.append(elem.field)
        result_lst.append(elem.pub_date.strftime("%Y-%m-%d"))
        result_lst.append(elem.period)
        result_lst.append(elem.status)
        result_lst.append(elem.views)
        view_ordered_posts_lst.append(result_lst)
        
    context = {'columns' : columns, 'posts': view_ordered_posts_lst, 'site_name': '상상대로 서울'}
    return render(request, "chart/uniform_charts.html", context)

def subthink_chart(request):
    participants_ordered_posts = SubThink.objects.order_by("-participants")[:10]


    columns = ['제목', '작성일', '기간', '참여자수', '추천/비추천']
    participants_ordered_posts_lst = []

    for elem in participants_ordered_posts:
        result_lst = []
        result_lst.append((elem.title, elem.url))
        result_lst.append(elem.pub_date.strftime("%Y-%m-%d"))
        start_date_str = elem.start_date.strftime("%Y-%m-%d")
        end_date_str = elem.end_date.strftime("%Y-%m-%d")
        result_lst.append(f"{start_date_str} ~ {end_date_str}")
        result_lst.append(elem.participants)
        result_lst.append(f"{elem.recommends}/{elem.no_recommends}")
        participants_ordered_posts_lst.append(result_lst)
        
    context = {'columns' : columns, 'posts': participants_ordered_posts_lst, 'site_name': '국민 생각함'}
    return render(request, "chart/uniform_charts.html", context)

def search_main(request):
    current_date = datetime.now().date()
    year_date = current_date - timedelta(days=365)

    context = {
        'current_date' : current_date,
        'year_date' : year_date
    }

    return render(request, "chart/search.html", context)

def search_result(request):
    current_date = datetime.now().date()
    year_date = current_date - timedelta(days=365)

    title = request.GET.get('title')
    s_date = request.GET.get('s_date')
    e_date = request.GET.get('e_date')
    site1 = request.GET.get('site1')
    site2 = request.GET.get('site2')
    site3 = request.GET.get('site3')

    f_list = []
    if site1:
        title_list = Congress.objects.filter(title__contains=title, pub_date__range=[s_date, e_date]).values('title', 'pub_date', 'url')
        for da in title_list:
            da['where'] = '국민동의청원'
            f_list.append(da)

    if site2:
        title_list = CW24.objects.filter(title__contains=title, pub_date__range=[s_date, e_date]).values('title', 'pub_date', 'url')
        for da in title_list:
            da['where'] = '청원24'
            f_list.append(da)

    if site3:
        title_list = SubThink.objects.filter(title__contains=title, pub_date__range=[s_date, e_date]).values('title', 'pub_date', 'url')
        for da in title_list:
            da['where'] = '국민 생각함'
            f_list.append(da)

    f_list = sorted(f_list, key=lambda x: x['pub_date'], reverse=True)

    context = {
        'title' : title,
        'posts': f_list,
        'current_date' : e_date,
        'year_date' : s_date,
        'site1' : site1,
        'site2' : site2,
        'site3' : site3
    }
    return render(request, "chart/search_result.html", context)