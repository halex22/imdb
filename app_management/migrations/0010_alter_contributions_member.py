# Generated by Django 4.1.3 on 2023-09-06 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_management', '0009_remove_artist_active_members_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributions',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='app_management.member'),
        ),
    ]
