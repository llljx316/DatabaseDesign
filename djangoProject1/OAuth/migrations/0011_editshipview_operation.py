# Generated by Django 4.2.13 on 2024-06-14 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OAuth', '0010_alter_shiproutepoint_ship_editshipview_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='editshipview',
            name='operation',
            field=models.CharField(choices=[('edit', 'Edit'), ('create', 'Create')], default='edit', max_length=6),
            preserve_default=False,
        ),
    ]
