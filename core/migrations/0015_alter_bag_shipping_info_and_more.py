# Generated by Django 4.2.13 on 2024-07-30 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_bagitem_bag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bag',
            name='shipping_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.shippinginfo'),
        ),
        migrations.AlterField(
            model_name='shippinginfo',
            name='governorate',
            field=models.CharField(choices=[('cairo', 'Cairo'), ('giza', 'Giza'), ('alexandria', 'Alexandria'), ('north_coast', 'North Coast')], max_length=255),
        ),
    ]
