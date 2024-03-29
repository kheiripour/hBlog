# Generated by Django 3.2.16 on 2022-12-10 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_auto_20221210_1543"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="about",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="profile",
            name="address",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(blank=True, default="", upload_to=""),
        ),
        migrations.AlterField(
            model_name="profile",
            name="phone_number",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
    ]
