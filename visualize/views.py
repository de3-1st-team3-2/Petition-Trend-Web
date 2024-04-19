from django.shortcuts import render
from .models import *
from datetime import datetime, timedelta
from wordcloud import WordCloud
from django.http import HttpResponse
import visualization_data_store.models

def generate_wordcloud(request,site):
    # 각 사이트에 해당하는 모델을 선택합니다.


    # 모델에서 필요한 데이터를 가져옵니다.
    texts = visualization_data_store.models.MonthlySitewiseWordCount.objects.filter(source=site).values_list('word', flat=True)
    text = ' '.join(texts)
    
    # WordCloud 객체를 생성하고, generate_from_text() 함수를 사용하여 워드클라우드를 생성합니다.
    font_path = "C:\Windows\Fonts\gulim.ttc"
    wordcloud = WordCloud(font_path=font_path,prefer_horizontal=2.0, background_color='white', width=800, height=400).generate_from_text(text)

    # 워드클라우드 이미지를 HttpResponse 객체로 반환합니다.
    response = HttpResponse(content_type="image/png")
    wordcloud.to_image().save(response, "PNG")
    
    return response


def main_index(request):
    
    return render(request, "chart/index.html")

def get_monthly_site_writes(site):
    if site == 'total':
        pass
    else:
        current_month_start = datetime(2023,1,1)
        monthly_writes_lst = visualization_data_store.models.MonthlySitewiseWrites.objects.values_list("date", site).filter(date__gte=current_month_start)
        bar_labels = []
        data_labels = []
        for label, data in monthly_writes_lst:
            bar_labels.append(label.strftime("%Y-%m-%d"))
            data_labels.append(data)
        return bar_labels, data_labels

def get_detail_chart_search_period(request):
    s_date = request.GET.get('s_date')
    e_date = request.GET.get('e_date')
    if s_date is None or e_date is None:
        e_date = datetime.now().date()
        s_date = (e_date - timedelta(days=30)).strftime("%Y-%m-%d")
        e_date = e_date.strftime("%Y-%m-%d")
    return s_date, e_date

def epeople_chart(request):
    s_date, e_date = get_detail_chart_search_period(request)
    order_by = request.GET.get("order-by")
    if order_by == 'rating':
        view_ordered_posts = Epeople.objects.filter(pub_date__gte=s_date, pub_date__lte=e_date).order_by("-rating")[:10]
    else:
        view_ordered_posts = Epeople.objects.filter(pub_date__gte=s_date, pub_date__lte=e_date).order_by("-views")[:10]

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
        


    bar_labels, bar_datas = get_monthly_site_writes("epeople")
               
    context = {'columns': columns, 'posts': view_ordered_posts_lst, 'site_name': '국민 신문고', 'wordcloud_url': '/generate_wordcloud/epeople','bar_labels': bar_labels, 'bar_datas': bar_datas}
    context['year_date'] = s_date
    context['current_date'] = e_date
    return render(request, "chart/uniform_charts.html", context)

def congress_chart(request):
    s_date, e_date = get_detail_chart_search_period(request)
    order_by = request.GET.get("order-by")
    view_ordered_posts = Congress.objects.filter(pub_date__gte=s_date, pub_date__lte=e_date).order_by("-rating")[:10]

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
    
    bar_labels, bar_datas = get_monthly_site_writes("congress")
    context = {'columns' : columns, 'posts': view_ordered_posts_lst, 'site_name': '국회 국민 동의 청원','wordcloud_url': '/generate_wordcloud/congress',
               'bar_labels': bar_labels, 'bar_datas': bar_datas}
    context['year_date'] = s_date
    context['current_date'] = e_date
    return render(request, "chart/uniform_charts.html", context)


def cw24_chart(request):
    s_date, e_date = get_detail_chart_search_period(request)
    view_ordered_posts = CW24.objects.filter(pub_date__gte=s_date, pub_date__lte=e_date).order_by("-views")[:10]

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
        
    bar_labels, bar_datas = get_monthly_site_writes("cw24")
    context = {'columns' : columns, 'posts': view_ordered_posts_lst, 'site_name': '청원 24','wordcloud_url': '/generate_wordcloud/cw24',
               'bar_labels': bar_labels, 'bar_datas': bar_datas}
    context['year_date'] = s_date
    context['current_date'] = e_date
    return render(request, "chart/uniform_charts.html", context)

def ideaseoul_chart(request):
    s_date, e_date = get_detail_chart_search_period(request)
    order_by = request.GET.get("order-by")
    view_ordered_posts = Ideaseoul.objects.filter(pub_date__gte=s_date, pub_date__lte=e_date).order_by("-views")[:10]

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
        
    bar_labels, bar_datas = get_monthly_site_writes("ideaseoul")
    context = {'columns' : columns, 'posts': view_ordered_posts_lst, 'site_name': '상상대로 서울','wordcloud_url': '/generate_wordcloud/ideaseoul',
               'bar_labels': bar_labels, 'bar_datas': bar_datas}
    context['year_date'] = s_date
    context['current_date'] = e_date
    return render(request, "chart/uniform_charts.html", context)

def subthink_chart(request):
    s_date, e_date = get_detail_chart_search_period(request)
    participants_ordered_posts = SubThink.objects.filter(pub_date__gte=s_date, pub_date__lte=e_date).order_by("-participants")[:10]


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
    
    bar_labels, bar_datas = get_monthly_site_writes("subthink")
    context = {'columns' : columns, 'posts': participants_ordered_posts_lst, 'site_name': '국민 생각함','wordcloud_url': '/generate_wordcloud/sub-think',
               'bar_labels': bar_labels, 'bar_datas': bar_datas}
    context['year_date'] = s_date
    context['current_date'] = e_date
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
    site4 = request.GET.get('site4')
    site5 = request.GET.get('site5')

    f_list = []
    if site1:
        title_list = Epeople.objects.filter(title__contains=title, pub_date__range=[s_date, e_date]).values('title', 'pub_date', 'url')
        for da in title_list:
            da['where'] = '국민 신문고'
            f_list.append(da)

    if site2:
        title_list = Congress.objects.filter(title__contains=title, pub_date__range=[s_date, e_date]).values('title', 'pub_date', 'url')
        for da in title_list:
            da['where'] = '국민동의청원'
            f_list.append(da)

    if site3:
        title_list = CW24.objects.filter(title__contains=title, pub_date__range=[s_date, e_date]).values('title', 'pub_date', 'url')
        for da in title_list:
            da['where'] = '청원24'
            f_list.append(da)

    if site4:
        title_list = Ideaseoul.objects.filter(title__contains=title, pub_date__range=[s_date, e_date]).values('title', 'pub_date', 'url')
        for da in title_list:
            da['where'] = '상상대로 서울'
            f_list.append(da)

    if site5:
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
        'site3' : site3,
        'site4' : site4,
        'site5' : site5
    }
    return render(request, "chart/search_result.html", context)