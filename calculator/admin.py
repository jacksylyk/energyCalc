from django.contrib import admin

from .models import Client, Contact, Invoice


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'bin_number', 'contract_number', 'contract_date', 'location')
    search_fields = ('name', 'bin_number', 'contract_number', 'location')
    list_filter = ('contract_date',)
    inlines = [ContactInline]


admin.site.register(Invoice)
admin.site.register(Client, ClientAdmin)
