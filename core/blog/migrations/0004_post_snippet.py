# Generated by Django 3.2.16 on 2022-12-15 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='snippet',
            field=models.TextField(default='Summary description for blogs page'),
        ),
    ]
