# Generated by Django 4.2.13 on 2024-08-03 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_bag_options_remove_shippinginfo_building_no_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bagitem',
            options={'verbose_name_plural': 'items'},
        ),
        migrations.AlterField(
            model_name='shippinginfo',
            name='bag',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.bag'),
        ),
    ]
