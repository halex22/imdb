# Generated by Django 4.1.3 on 2023-09-05 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_management', '0005_album_contributors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='contributors',
        ),
        migrations.DeleteModel(
            name='AlbumContributor',
        ),
    ]