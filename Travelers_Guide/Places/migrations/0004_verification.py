# Generated by Django 2.2.2 on 2019-06-23 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Places', '0003_placereview'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('temp_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('nationality', models.CharField(max_length=50)),
                ('passport_no', models.CharField(blank=True, max_length=250)),
                ('gender', models.CharField(max_length=6)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=20)),
                ('otp', models.IntegerField(blank=True, max_length=4)),
            ],
            options={
                'db_table': 'Verifications',
            },
        ),
    ]
