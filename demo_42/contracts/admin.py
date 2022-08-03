from django.contrib import admin

from .models import Partner, Contract


class PartnerAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'slug',
        'description',
    )
    list_editable = ('title', 'description',)
    search_fields = ('title',)
    empty_value_display = '-пусто-'


class ContractAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'number',
        'start_date',
        'end_date',
        'curator',
        'partner',
    )
    list_editable = ('curator', 'partner',)
    search_fields = ('number',)
    list_filter = ('start_date', 'end_date',)
    empty_value_display = '-пусто-'


admin.site.register(Partner, PartnerAdmin)
admin.site.register(Contract, ContractAdmin)
