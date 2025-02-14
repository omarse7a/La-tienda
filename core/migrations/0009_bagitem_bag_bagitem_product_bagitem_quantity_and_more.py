# Generated by Django 4.2.13 on 2024-07-17 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_bag_bagitem_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bagitem',
            name='bag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.bag'),
        ),
        migrations.AddField(
            model_name='bagitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.product'),
        ),
        migrations.AddField(
            model_name='bagitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
