# Generated by Django 5.0.6 on 2024-06-24 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_suscripcion_fecha_inicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='suscripcion',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='suscripcion',
            name='precio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='suscripcion',
            name='stock',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='suscripcion',
            name='ventas',
            field=models.IntegerField(default=0),
        ),
    ]
