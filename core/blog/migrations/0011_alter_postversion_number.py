# Generated by Django 3.2.16 on 2022-12-21 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_postversion_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postversion',
            name='number',
            field=models.PositiveSmallIntegerField(blank=True),
        ),
    ]