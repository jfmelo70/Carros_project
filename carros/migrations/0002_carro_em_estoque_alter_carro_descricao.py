# Generated by Django 5.1.1 on 2024-11-28 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carros', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carro',
            name='em_estoque',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='carro',
            name='descricao',
            field=models.TextField(blank=True, null=True),
        ),
    ]
