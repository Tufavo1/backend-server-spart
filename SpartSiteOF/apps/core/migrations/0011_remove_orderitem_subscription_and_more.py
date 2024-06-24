# Generated by Django 5.0.6 on 2024-06-24 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_orderitem_subscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='subscription',
        ),
        migrations.AddField(
            model_name='producto',
            name='es_suscripcion',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.DeleteModel(
            name='Suscripcion',
        ),
    ]