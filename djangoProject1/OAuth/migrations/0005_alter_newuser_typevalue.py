# Generated by Django 3.2.15 on 2024-06-10 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OAuth', '0004_newuser_typevalue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='typevalue',
            field=models.PositiveSmallIntegerField(choices=[(1, 'admin'), (2, 'shipcrew'), (3, 'analyst'), (4, 'supervisor')]),
        ),
    ]
