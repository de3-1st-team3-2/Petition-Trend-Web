# Generated by Django 4.2.6 on 2024-04-19 04:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("visualize", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubThink",
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
                ("title", models.CharField(max_length=50, verbose_name="제목")),
                ("url", models.CharField(max_length=200, verbose_name="URL")),
                ("pub_date", models.DateTimeField(verbose_name="작성일")),
                ("start_date", models.DateTimeField(verbose_name="시작일")),
                ("end_date", models.DateTimeField(verbose_name="종료일")),
                ("participants", models.IntegerField(null=True, verbose_name="참여자수")),
                ("recommends", models.IntegerField(null=True, verbose_name="추천수")),
                ("no_recommends", models.IntegerField(null=True, verbose_name="비추천수")),
            ],
        ),
    ]
