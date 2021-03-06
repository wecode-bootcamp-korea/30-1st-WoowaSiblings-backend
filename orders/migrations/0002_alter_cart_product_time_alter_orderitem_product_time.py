# Generated by Django 4.0.2 on 2022-03-08 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product_time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.producttime'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product_time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.producttime'),
        ),
    ]
