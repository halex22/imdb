# Generated by Django 4.1.3 on 2023-09-05 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_management', '0006_remove_album_contributors_delete_albumcontributor'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='active_members',
            field=models.ManyToManyField(related_name='active_members', to='app_management.member'),
        ),
        migrations.AddField(
            model_name='artist',
            name='all_members',
            field=models.ManyToManyField(related_name='all_members', to='app_management.member'),
        ),
    ]
