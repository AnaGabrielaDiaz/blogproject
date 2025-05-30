# Generated by Django 5.2 on 2025-04-21 19:36

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_alter_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='featured_image',
            field=models.ImageField(blank=True, null=True, upload_to='featured_images/'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
