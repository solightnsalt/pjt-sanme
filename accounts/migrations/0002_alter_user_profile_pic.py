# Generated by Django 3.2.13 on 2022-11-21 08:17

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=imagekit.models.fields.ProcessedImageField(null=True, upload_to='profile/%Y%m%d/'),
        ),
    ]
