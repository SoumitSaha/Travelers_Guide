# Generated by Django 2.2.1 on 2019-09-13 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Places', '0023_place_aveage_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='aveage_rating',
            field=models.CharField(default=0, max_length=1),
        ),
    ]
