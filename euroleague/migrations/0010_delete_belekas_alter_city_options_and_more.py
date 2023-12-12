# Generated by Django 5.0 on 2023-12-12 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('euroleague', '0009_alter_league_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='belekas',
        ),
        migrations.AlterModelOptions(
            name='city',
            options={},
        ),
        migrations.AlterModelOptions(
            name='gamestats',
            options={},
        ),
        migrations.AlterModelOptions(
            name='profilis',
            options={'verbose_name': 'Profile', 'verbose_name_plural': 'Profile'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={},
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(help_text='City name', max_length=200),
        ),
        migrations.AlterField(
            model_name='league',
            name='description',
            field=models.TextField(blank=True, help_text='League description', max_length=1000),
        ),
        migrations.AlterField(
            model_name='league',
            name='name',
            field=models.CharField(help_text='League name', max_length=200),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(help_text='Team name', max_length=200),
        ),
        migrations.AlterField(
            model_name='team',
            name='summary',
            field=models.TextField(help_text='Team summary', max_length=1000),
        ),
    ]