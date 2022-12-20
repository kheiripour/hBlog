# Generated by Django 3.2.16 on 2022-12-20 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20221219_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='active_version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='blog.postversion'),
        ),
        migrations.AlterField(
            model_name='postversion',
            name='snippet',
            field=models.TextField(default='Summary description for blogs page', max_length=150),
        ),
    ]