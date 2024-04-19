from django.db import models

# Create your models here.

class MonthlySitewiseWrites(models.Model):
    date = models.DateTimeField(verbose_name="날짜")
    epeople = models.IntegerField(verbose_name="국민신문고")
    congress = models.IntegerField(verbose_name="국회 국민 동의 청원")
    ideaseoul = models.IntegerField(verbose_name="아이디어 서울")
    cw24 = models.IntegerField(verbose_name="청원 24")
    subthink = models.IntegerField(verbose_name="국민 생각함")

class MonthlySitewiseWordCount(models.Model):
    word = models.CharField(max_length=30, verbose_name="단어")
    cnt = models.IntegerField(verbose_name="빈도")
    source = models.CharField(max_length=25, verbose_name="출처")
    date = models.DateTimeField(verbose_name="날짜")
