# Generated by Django 2.2.2 on 2019-07-23 16:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Places', '0015_tourist_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='placereview',
            name='tourist_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=250),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='PlaceSuggestion',
            fields=[
                ('suggestion_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('category', models.CharField(max_length=50)),
                ('gps_x', models.CharField(max_length=250)),
                ('gps_y', models.CharField(max_length=250)),
                ('opening_time', models.TimeField(blank=True, null=True)),
                ('closing_time', models.TimeField(blank=True, null=True)),
                ('offday', models.CharField(blank=True, max_length=10, null=True)),
                ('sample_pic', models.CharField(max_length=500)),
                ('suggested_location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Places.Location')),
            ],
            options={
                'db_table': 'PlaceSuggestions',
            },
        ),
    ]
