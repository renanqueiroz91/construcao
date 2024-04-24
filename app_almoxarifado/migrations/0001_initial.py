# Generated by Django 5.0.4 on 2024-04-24 13:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Construcao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(max_length=100)),
                ('tipo_material', models.CharField(default='und', max_length=20)),
                ('quantidade', models.PositiveIntegerField(default=0)),
                ('construcao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_almoxarifado.construcao')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('und', 'Unidade'), ('caixa', 'Caixa'), ('rolo', 'Rolo'), ('par', 'Par'), ('kg', 'Quilograma'), ('metro', 'Metro')], max_length=20)),
                ('construcao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_almoxarifado.construcao')),
            ],
        ),
    ]
