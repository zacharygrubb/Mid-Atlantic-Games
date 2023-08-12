# Generated by Django 3.2.3 on 2022-07-11 23:27

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20220612_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='cover_image',
            field=models.ImageField(default='games/empty_cover.jpg', upload_to=store.models.cover_upload_path),
        ),
        migrations.AlterField(
            model_name='game',
            name='genre',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='game',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
