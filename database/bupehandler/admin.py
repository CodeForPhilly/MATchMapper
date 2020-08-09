from django.contrib import admin
from .models import Address, Affiliate, Email, Licence, Npi, Phone, ProvSiteRef, Provider, Site, Xwaiver


# Register your models here.

admin.site.register(Address)
admin.site.register(Affiliate)
admin.site.register(Email)
admin.site.register(Licence)
admin.site.register(Npi)
admin.site.register(Phone)
admin.site.register(ProvSiteRef)
admin.site.register(Provider)
admin.site.register(Site)
admin.site.register(Xwaiver)

