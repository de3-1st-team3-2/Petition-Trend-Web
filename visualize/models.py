from django.db import models

# Create your models here.

class Epeople(models.Model):
    title = models.CharField(max_length=50, verbose_name="제목")
    url = models.CharField(max_length=100, verbose_name="URL")
    agency = models.CharField(max_length=10, verbose_name="처리기관")
    pub_date = models.DateTimeField(verbose_name="작성일")
    status = models.CharField(max_length=10, verbose_name="추진상황")
    views = models.IntegerField(verbose_name="조회수")
    rating = models.FloatField(verbose_name="평점")
    field = models.CharField(max_length=50, verbose_name="분야")
    content = models.CharField(max_length=300, verbose_name="내용")

class Congress(models.Model):
    title = models.CharField(max_length=50, verbose_name="제목")
    pub_date = models.DateTimeField(verbose_name="작성일")
    url = models.CharField(max_length=100, verbose_name="URL")
    agency = models.CharField(max_length=20, verbose_name="처리기관")
    status = models.CharField(max_length=20, null=True, verbose_name="추진상황")
    rating = models.IntegerField(verbose_name="동의수")
    category = models.CharField(max_length=20, verbose_name="분야")

    def __str__(self):
        return f"제목: {self.title}, 작성일: {self.pub_date}, 추진상황: {self.status}"


class Ideaseoul(models.Model):
    title = models.CharField(max_length=50, verbose_name="제목")
    url = models.CharField(max_length=100, verbose_name="URL")
    pub_date = models.DateTimeField(verbose_name="작성일")
    period = models.CharField(max_length=50, verbose_name="기간")
    status = models.CharField(max_length=10, verbose_name="추진상황")
    views = models.IntegerField(verbose_name="조회수")
    field = models.CharField(max_length=50, verbose_name="분야")
    content = models.CharField(max_length=300, verbose_name="내용")
    def __str__(self):
        return f"제목: {self.title}, 작성일: {self.pub_date}, 추진상황: {self.status}"

class CW24(models.Model):
    title = models.CharField(max_length=50, verbose_name="제목")
    url = models.CharField(max_length=200, verbose_name="URL")
    agency = models.CharField(max_length=10, verbose_name="처리기관")
    pub_date = models.DateTimeField(verbose_name="작성일")
    start_date = models.DateTimeField(verbose_name="시작일")
    end_date = models.DateTimeField(verbose_name="종료일")
    status = models.CharField(null = True, max_length=20, verbose_name="추진상황")
    views = models.IntegerField(null = True, verbose_name="조회수")
    content = models.CharField(null = True, max_length=300, verbose_name="내용")
    comment_num = models.IntegerField(null = True, verbose_name="댓글수")
    result = models.CharField(max_length=300, null = True, verbose_name="처리결과")

    def __str__(self):
        return f"제목: {self.title}, 작성일: {self.pub_date}, 추진상황: {self.status}"
    
class SubThink(models.Model):
    title = models.CharField(max_length=50, verbose_name="제목")
    url = models.CharField(max_length=200, verbose_name="URL")
    pub_date = models.DateTimeField(verbose_name="작성일")
    start_date = models.DateTimeField(verbose_name="시작일")
    end_date = models.DateTimeField(verbose_name="종료일")
    participants = models.IntegerField(null = True, verbose_name="참여자수")
    recommends = models.IntegerField(null = True, verbose_name="추천수")
    no_recommends = models.IntegerField(null = True, verbose_name="비추천수")

    def __str__(self):
        return f"제목: {self.title}, 작성일: {self.pub_date}, 추진상황: {self.status}"
    