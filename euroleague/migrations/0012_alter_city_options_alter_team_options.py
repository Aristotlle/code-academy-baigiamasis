# Generated by Django 5.0 on 2023-12-12 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('euroleague', '0011_alter_euroleaguefact_options_alter_gamestats_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'City', 'verbose_name_plural': 'City'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'verbose_name': 'Team', 'verbose_name_plural': 'Team'},
        ),
    ]