# Generated by Django 4.1.3 on 2023-08-25 11:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('genre', models.CharField(max_length=25)),
                ('added_date', models.DateField(default=django.utils.timezone.now)),
                ('fundation_date', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(limit_value=1950, message='No artist before 1950'), django.core.validators.MaxValueValidator(limit_value=2023, message="Can't enter a higher than the current year")])),
                ('img', models.ImageField(blank=True, null=True, upload_to='images')),
                ('subgenres', models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('released_date', models.DateField()),
                ('added_date', models.DateField(default=django.utils.timezone.now)),
                ('img', models.ImageField(blank=True, null=True, upload_to='images')),
                ('n_votes', models.IntegerField(default=0)),
                ('rating', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(limit_value=0, message='The lowest rate is 0'), django.core.validators.MaxValueValidator(limit_value=10, message='The highest rate is 10')])),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='app_management.artist')),
            ],
        ),
    ]
