from django import forms
from django.contrib import admin, messages
from .models import Personal, Key, KeyHandover, KeyReception
from django.core.exceptions import ObjectDoesNotExist
from import_export.admin import ExportActionMixin

@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    search_fields = ['name','email', 'phone', 'code']
    list_display = ['name', 'email', 'phone']

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'code':
            field.widget.attrs['onkeydown'] = 'if (event.keyCode == 13) { event.preventDefault(); return false; }'
        return field


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    search_fields = ['code', 'number']


@admin.register(KeyHandover)
class KeyHandoverAdmin(ExportActionMixin, admin.ModelAdmin):
    search_fields = ['personal_code', 'key_code']
    list_display = ['get_id', 'get_personal_name', 'get_document_number', 'get_timestamp', 'get_key_number', 'get_status_display']
    list_filter = ['timestamp']
    fields = ('personal_code', 'key_code')  # Campos a mostrar en el formulario del admin

    def get_id(self, obj):
        return obj.id
    
    def get_personal_name(self, obj):
        return obj.personal.name
    
    def get_document_number(self, obj):
        return obj.personal.document_number

    def get_timestamp(self, obj):
        return obj.timestamp
    
    def get_key_number(self, obj):
        return obj.key.number

    get_id.short_description = 'Evento'
    get_personal_name.short_description = 'Nombre'
    get_document_number.short_description = 'Cédula'
    get_timestamp.short_description = 'Fecha'
    get_key_number.short_description = 'Llave entregada'
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'personal_code':
            field.widget.attrs['onkeydown'] = 'if (event.keyCode == 13) { event.preventDefault(); return false; }'
        return field

    def save_model(self, request, obj, form, change):
        
        try:
            # Buscar las instancias relacionadas por el código
            personal = Personal.objects.get(code=obj.personal_code)
            key = Key.objects.get(code=obj.key_code)
            # Asignar las referencias FK
            obj.personal = personal
            obj.key = key
            # Guardar el objeto KeyHandover
            obj.save()
        except ObjectDoesNotExist:
            messages.error(request, "No se encuentran estos códigos en la base de Datos.")

@admin.register(KeyReception)
class KeyReceptionAdmin(admin.ModelAdmin):
    search_fields = ['personal_code', 'key_code']
    list_display = ['key', 'personal', 'timestamp']
    list_filter = ['timestamp']
    fields = ('key_code',)  # Campos a mostrar en el formulario del admin

    def save_model(self, request, obj, form, change):
        try:
            key = Key.objects.get(code=obj.key_code)
            key_handover = KeyHandover.objects.get(key=key, status='pendiente')
            obj.personal = key_handover.personal
            obj.key = key
            key_handover.status = 'entregado'
            key_handover.save()
            obj.save()
        except ObjectDoesNotExist:
            messages.error(request, "Esta llave no existe o ya ha sido devuelta.")

admin.site.site_header = "Administración"
admin.site.site_title = "Administración"
admin.site.index_title = "Administración"