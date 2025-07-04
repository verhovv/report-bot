# Generated by Django 5.2.1 on 2025-06-06 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0003_alter_publication_file_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='day_report',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='group',
            name='evening_report',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='field',
            name='type',
            field=models.CharField(choices=[('int', 'Целое число'), ('float', 'Дробное число'), ('date', 'Дата'), ('str', 'Текст')], verbose_name='Тип поля'),
        ),
    ]
