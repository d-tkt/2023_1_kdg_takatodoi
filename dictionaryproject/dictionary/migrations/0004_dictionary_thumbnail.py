# Generated by Django 4.1.3 on 2023-12-14 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0003_remove_dictionary_id_alter_dictionary_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='dictionary',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
