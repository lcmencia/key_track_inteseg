from django import forms
from django.contrib import admin, messages
from .models import Personal, Key, KeyHandover, KeyReception
from django.core.exceptions import ObjectDoesNotExist

@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    search_fields = ['name','email', 'phone', 'code']
    list_display = ['name', 'email', 'phone']

@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    search_fields = ['code', 'number']


@admin.register(KeyHandover)
class KeyHandoverAdmin(admin.ModelAdmin):
    search_fields = ['personal_code', 'key_code']
    list_display = ['key', 'personal', 'timestamp', 'get_status_display']
    list_filter = ['timestamp']
    fields = ('personal_code', 'key_code')  # Campos a mostrar en el formulario del admin

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