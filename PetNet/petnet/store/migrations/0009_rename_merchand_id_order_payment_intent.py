# Generated by Django 4.1.7 on 2023-04-04 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_order_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='merchand_id',
            new_name='payment_intent',
        ),
    ]