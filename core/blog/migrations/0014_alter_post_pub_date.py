# Generated by Django 3.2.16 on 2022-12-22 06:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0013_alter_postversion_post"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="pub_date",
            field=models.DateField(
                blank=True, default=datetime.date(2022, 12, 22), null=True
            ),
        ),
    ]
