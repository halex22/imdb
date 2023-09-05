# Generated by Django 4.1.3 on 2023-09-05 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_management', '0004_member_nickname_alter_member_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='contributors',
            field=models.ManyToManyField(related_name='contributed_albums', through='app_management.AlbumContributor', to='app_management.member'),
        ),
    ]
