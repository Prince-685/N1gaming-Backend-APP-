# Generated by Django 5.0.6 on 2024-06-03 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='win_percent',
            name='percent',
            field=models.IntegerField(default=80),
        ),
    ]