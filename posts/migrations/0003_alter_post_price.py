# Generated by Django 4.1.5 on 2023-05-03 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_remove_post_street_alter_post_facing_side'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='price',
            field=models.FloatField(),
        ),
    ]
