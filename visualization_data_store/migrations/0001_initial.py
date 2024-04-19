# Generated by Django 4.2.6 on 2024-04-19 04:29

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MonthlySitewiseWordCount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("word", models.CharField(max_length=30, verbose_name="단어")),
                ("cnt", models.IntegerField(verbose_name="빈도")),
                ("source", models.CharField(max_length=25, verbose_name="출처")),
                ("date", models.DateTimeField(verbose_name="날짜")),
            ],
        ),
        migrations.CreateModel(
            name="MonthlySitewiseWrites",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField(verbose_name="날짜")),
                ("epeople", models.IntegerField(verbose_name="국민신문고")),
                ("congress", models.IntegerField(verbose_name="국회 국민 동의 청원")),
                ("ideaseoul", models.IntegerField(verbose_name="아이디어 서울")),
                ("cw24", models.IntegerField(verbose_name="청원 24")),
                ("subthink", models.IntegerField(verbose_name="국민 생각함")),
            ],
        ),
    ]