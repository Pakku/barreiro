# Generated by Django 3.0.7 on 2020-06-14 18:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=filer.fields.image.FilerImageField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_images', to=settings.FILER_IMAGE_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='summary',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
