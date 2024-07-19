# Generated by Django 5.0.6 on 2024-07-18 16:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0002_remove_appliance_user_remove_energyusage_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appliance',
            name='group',
        ),
        migrations.RemoveField(
            model_name='energyusage',
            name='group',
        ),
        migrations.AddField(
            model_name='appliance',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='energyusage',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='appliance',
            name='name',
            field=models.CharField(blank=True, default='Refrigerator', max_length=100),
        ),
        migrations.DeleteModel(
            name='Group',
        ),
    ]
