# Generated by Django 3.2.16 on 2022-12-11 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='profiles/default.png', height_field='image_size', null=True, upload_to='profiles/', width_field='image_size'),
        ),
    ]
