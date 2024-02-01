# Generated by Django 5.0.1 on 2024-01-31 12:00

import mainapp.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0002_post_file_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="post",
            field=models.FileField(
                upload_to="images", validators=[mainapp.models.validate_file_extensions]
            ),
        ),
    ]