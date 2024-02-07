# Generated by Django 4.1.3 on 2024-01-05 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('composite', '0003_remove_item_id_alter_composite_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composite',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='composite_items', to='composite.item'),
        ),
        migrations.AlterField(
            model_name='composite',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='composite_materials', to='composite.item'),
        ),
    ]