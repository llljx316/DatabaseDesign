# Generated by Django 4.2.13 on 2024-06-13 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OAuth', '0008_shiproutepoint'),
    ]

    operations = [
        migrations.AddField(
            model_name='shiproutepoint',
            name='direction',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='shiproutepoint',
            name='next_node',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous_nodes', to='OAuth.shiproutepoint'),
        ),
        migrations.AddField(
            model_name='shiproutepoint',
            name='speed',
            field=models.FloatField(null=True),
        ),
    ]
