# Generated by Django 3.2.16 on 2022-12-22 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_postversion_post'),
        ('website', '0008_rename_id_done_contact_is_done'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('category', models.ManyToManyField(to='blog.Category')),
            ],
        ),
    ]
