from django.contrib import admin

from .models import Client, Letter, Package, PostOffice


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'lastname', 'middle_name', 'phone_number',)


@admin.register(PostOffice)
class PostOfficeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'address', 'postal_index',)
    search_fields = ('address',)


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'sender',
                    'recipient',
                    'departure_office',
                    'arrival_office',
                    'category',
                    'weight',)
    search_fields = ('departure_office__address',
                     'arrival_office__address',)
    list_filter = ('category',)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'sender',
                    'recipient',
                    'departure_office',
                    'arrival_office',
                    'category',
                    'cost',)
    search_fields = ('departure_office__address',
                     'arrival_office__address',)
    list_filter = ('category',)
