# Generated by Django 3.0.5 on 2020-04-26 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0008_auto_20200426_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='feedbacks/%Y/%m/%d/'),
        ),
    ]
