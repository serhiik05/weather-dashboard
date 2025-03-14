# Generated by Django 5.1.4 on 2025-03-11 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(db_index=True, max_length=100)),
                ('temperature', models.FloatField()),
                ('humidity', models.PositiveSmallIntegerField()),
                ('wind_speed', models.FloatField()),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('pressure', models.IntegerField(blank=True, null=True)),
                ('feels_like', models.FloatField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'ordering': ['-timestamp'],
                'indexes': [models.Index(fields=['city'], name='weather_wea_city_226bd6_idx'), models.Index(fields=['timestamp'], name='weather_wea_timesta_7bce59_idx')],
            },
        ),
    ]
