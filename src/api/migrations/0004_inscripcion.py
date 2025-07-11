# Generated by Django 5.2.3 on 2025-06-19 22:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_modulo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inscripcion', models.DateField(auto_now_add=True)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.curso')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.estudiante')),
            ],
        ),
    ]
