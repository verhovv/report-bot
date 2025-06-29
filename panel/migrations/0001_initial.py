# Generated by Django 5.2.1 on 2025-06-02 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='Идентификатор Телеграм')),
                ('username', models.CharField(blank=True, max_length=64, null=True, verbose_name='Юзернейм')),
                ('first_name', models.CharField(blank=True, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, null=True, verbose_name='Фамилия')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('data', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'verbose_name': 'Телеграм пользователь',
                'verbose_name_plural': 'Телеграм пользователи',
            },
        ),
    ]
