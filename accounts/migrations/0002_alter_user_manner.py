# Generated by Django 4.1.3 on 2022-11-10 08:12

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="manner",
            field=multiselectfield.db.fields.MultiSelectField(
                choices=[
                    ("활발", "활발한"),
                    ("조용", "조용한"),
                    ("애교", "애교가 넘치는"),
                    ("어른", "어른스러운"),
                    ("열정", "열정적인"),
                    ("침착", "침착한"),
                    ("예의", "예의바른"),
                    ("유머", "유머러스한"),
                    ("진지", "진지한"),
                    ("지적", "지적인"),
                    ("성실", "성실한"),
                    ("감성", "감성적인"),
                    ("꼼꼼", "꼼꼼한"),
                    ("논리", "논리적인"),
                    ("즉흥", "즉흥적인"),
                    ("소심", "소심한"),
                    ("쿨", "쿨한"),
                ],
                max_length=100,
            ),
        ),
    ]
