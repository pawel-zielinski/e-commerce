# Generated by Django 3.1.6 on 2021-05-11 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login_API', '0002_auto_20210511_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
