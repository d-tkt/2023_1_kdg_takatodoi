# Generated by Django 4.1.3 on 2023-12-12 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_dictionary_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dictionary',
            name='id',
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='title',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
