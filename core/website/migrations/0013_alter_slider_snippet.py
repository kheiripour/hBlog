# Generated by Django 3.2.16 on 2022-12-22 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0012_alter_newsletter_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="slider",
            name="snippet",
            field=models.TextField(
                blank=True,
                help_text="Leave it blank to use post snippet.",
                max_length=200,
            ),
        ),
    ]
