# Generated by Django 3.2.16 on 2022-12-22 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0016_alter_post_pub_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="pub_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
