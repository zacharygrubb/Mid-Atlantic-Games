# Generated by Django 3.2.3 on 2022-08-14 22:06

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='cover_image',
            field=models.FileField(default='games/empty_cover.jpg', upload_to=store.models.cover_upload_path),
        ),
        migrations.AlterField(
            model_name='post',
            name='cover_image',
            field=models.FileField(upload_to=store.models.cover_upload_blog_path),
        ),
        migrations.AlterField(
            model_name='post',
            name='image_one',
            field=models.FileField(blank=True, upload_to=store.models.upload_blog_path),
        ),
        migrations.AlterField(
            model_name='post',
            name='image_three',
            field=models.FileField(blank=True, upload_to=store.models.upload_blog_path),
        ),
        migrations.AlterField(
            model_name='post',
            name='image_two',
            field=models.FileField(blank=True, upload_to=store.models.upload_blog_path),
        ),
    ]
