# Generated by Django 4.1.7 on 2023-05-20 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_producto_stock_pro'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='estado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pedido',
            name='total',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]