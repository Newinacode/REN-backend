# Generated by Django 4.1.5 on 2023-04-30 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Land',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.CharField(choices=[('BY', 'buy'), ('SL', 'sell'), ('RT', 'rent')], max_length=2)),
                ('area_formating', models.CharField(choices=[('TE', 'terai'), ('HM', 'hilly and mountain')], max_length=2)),
                ('area1', models.IntegerField()),
                ('area2', models.IntegerField()),
                ('area3', models.IntegerField()),
                ('price', models.PositiveBigIntegerField()),
                ('property_type', models.CharField(default='L', max_length=1)),
                ('post', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.CharField(choices=[('BY', 'buy'), ('SL', 'sell'), ('RT', 'rent')], max_length=2)),
                ('area_formating', models.CharField(choices=[('TE', 'terai'), ('HM', 'hilly and mountain')], max_length=2)),
                ('area1', models.IntegerField()),
                ('area2', models.IntegerField()),
                ('area3', models.IntegerField()),
                ('price', models.PositiveBigIntegerField()),
                ('property_type', models.CharField(default='H', max_length=1)),
                ('no_of_bedrooms', models.IntegerField()),
                ('no_of_bathrooms', models.IntegerField()),
                ('no_of_floor', models.IntegerField()),
                ('parking_area', models.PositiveIntegerField()),
                ('facing_side', models.CharField(max_length=2)),
                ('built_date', models.DateField()),
                ('post', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
