# Generated by Django 4.1.3 on 2024-01-15 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('composite', '0008_alter_comp_list_comp_quantity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Previous_List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_quantity', models.PositiveIntegerField()),
                ('previous_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='composite_previous', to='composite.item')),
            ],
        ),
    ]
