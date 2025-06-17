from django.db import models


class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=64)

    def __str__(self):
        return self.username


class Field(models.Model):
    class FieldTypes(models.TextChoices):
        INTEGER = 'int', 'Целое число'
        FLOAT = 'float', 'Дробное число'
        DATE = 'date', 'Дата'
        TEXT = 'str', 'Текст'

    name = models.CharField('Название поля')
    type = models.CharField('Тип поля', choices=FieldTypes)

    def __str__(self):
        return f'{self.name} | {self.get_type_display()}'

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'


class Template(models.Model):
    name = models.CharField('Название', primary_key=True)
    fields = models.ManyToManyField(Field, verbose_name='Поля')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'


class Group(models.Model):
    id = models.BigIntegerField('Идентификатор группы', primary_key=True)
    name = models.CharField('Название группы (Опционально)', null=True, blank=True)
    main_username = models.CharField('Юзернейм ответственного')

    day_report = models.BooleanField(default=False)
    evening_report = models.BooleanField(default=False)
    tried = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} | {self.id} | {self.main_username}'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Publication(models.Model):
    class PublicationTypes(models.TextChoices):
        VIDEO = 'video', 'Видео'
        PHOTO = 'photo', 'Фото'

    text = models.TextField('Текст')
    type = models.CharField('Тип вложения', choices=PublicationTypes, null=True, blank=True)
    file = models.FileField('Вложение', upload_to='files/', null=True, blank=True)
    file_id = models.CharField(editable=False, null=True)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
