# Generated by Django 3.2.13 on 2022-11-16 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20221116_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='manner_point',
            field=models.FloatField(default=36.5),
        ),
    ]