# Generated by Django 3.0.5 on 2020-04-25 14:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0004_auto_20200424_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='date_stamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
