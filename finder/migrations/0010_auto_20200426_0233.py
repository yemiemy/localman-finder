# Generated by Django 3.0.5 on 2020-04-26 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0009_auto_20200426_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='image',
            field=models.ImageField(upload_to='feedbacks/%Y/%m/%d/'),
        ),
    ]
