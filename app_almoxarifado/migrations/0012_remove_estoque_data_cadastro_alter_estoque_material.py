# Generated by Django 5.0.4 on 2024-04-24 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_almoxarifado', '0011_estoque_data_cadastro_alter_estoque_material'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estoque',
            name='data_cadastro',
        ),
        migrations.AlterField(
            model_name='estoque',
            name='material',
            field=models.CharField(max_length=100),
        ),
    ]
