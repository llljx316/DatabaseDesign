# Generated by Django 4.2.13 on 2024-06-14 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OAuth', '0013_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiproutepoint',
            name='ship',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='OAuth.ship'),
            preserve_default=False,
        ),
    ]
