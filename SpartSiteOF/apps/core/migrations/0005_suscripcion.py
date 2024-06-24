# Generated by Django 5.0.6 on 2024-06-24 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_customuser_is_subscribed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suscripcion',
            fields=[
                ('sku', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('fecha_ingreso', models.DateField(auto_now_add=True)),
                ('fecha_expiracion', models.DateField(blank=True, null=True)),
                ('descripcion', models.CharField(max_length=255)),
                ('imagen', models.ImageField(upload_to='imgSuscripcion')),
                ('periodo', models.IntegerField(choices=[(1, '1 mes'), (3, '3 meses'), (5, '5 meses'), (12, '1 año')], default=1)),
            ],
        ),
    ]
