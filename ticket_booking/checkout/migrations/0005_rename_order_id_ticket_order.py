# Generated by Django 4.2.10 on 2024-02-27 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_rename_customer_ticket_order_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='order_id',
            new_name='order',
        ),
    ]
