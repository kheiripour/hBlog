# Generated by Django 3.2.16 on 2022-12-11 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0015_auto_20221211_1459"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="profiles/"),
        ),
    ]
