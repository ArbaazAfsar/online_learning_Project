# Generated by Django 5.0.7 on 2024-08-18 17:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_alter_course_image_alter_coursecategory_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lecture',
            options={},
        ),
        migrations.AddField(
            model_name='lecture',
            name='video_file',
            field=models.FileField(blank=True, null=True, upload_to='lectures/videos/', validators=[django.core.validators.FileExtensionValidator(['mp4', 'mov', 'avi'])]),
        ),
    ]
