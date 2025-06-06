from django.contrib import admin
from panel.models import *


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    fields = ('name', 'type')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'main_username')
    fields = ('name', 'id', 'main_username')


class FieldsInline(admin.TabularInline):
    model = Template.fields.through
    extra = 0

    verbose_name = 'Поле'
    verbose_name_plural = 'Поля'


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name',)
    inlines = (FieldsInline,)

    def has_delete_permission(self, request, obj=...):
        return False

    def has_add_permission(self, request, obj=...):
        return False


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('text', 'type', 'file')
    fields = ('text', 'type', 'file')
