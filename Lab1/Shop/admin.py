from django.contrib import admin

from Shop.models import *


class ProducerAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Producer, ProducerAdmin)


class OperationSystemAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(OperationSystem, OperationSystemAdmin)


class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Type, TypeAdmin)


class PhoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'producer', 'operation_system', 'type', 'multimedia', 'cost', 'image', 'description']
    list_filter = ['name']
    ordering = ['name']
    list_display_links = ['name', 'producer']

    @staticmethod
    def producer_name(obj):
        return obj.producer.name
admin.site.register(Phone, PhoneAdmin)
