# Generated by Django 2.2.1 on 2019-09-13 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Places', '0020_remove_placesuggestion_environment'),
    ]

    operations = [
        migrations.AddField(
            model_name='placesuggestion',
            name='average_rating',
            field=models.CharField(default='', max_length=1),
        ),
    ]
