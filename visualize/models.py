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