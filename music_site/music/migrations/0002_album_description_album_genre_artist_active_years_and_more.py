# Generated by Django 5.1.4 on 2024-12-16 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='album',
            name='genre',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='artist',
            name='active_years',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='artist',
            name='country',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='track',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='track',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
