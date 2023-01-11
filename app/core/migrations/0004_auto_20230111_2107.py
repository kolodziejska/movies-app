# Generated by Django 3.2.16 on 2023-01-11 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20230108_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='average_rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]