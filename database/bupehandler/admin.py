# from django.contrib import admin
# from .models import Address, Affiliate, Email, Licence, Npi, Phone, ProvSiteRef, Provider, Site, Xwaiver
from django.contrib import admin
from .models import Sites_all, Sitecodes_samhsa_ftloc,Siterecs_samhsa_ftloc, Siterecs_samhsa_otp, Siterecs_dbhids_tad, Siterecs_other_srcs, Siterecs_hfp_fqhc



# Register your models here.

admin.site.register(Sites_all)
admin.site.register(Sitecodes_samhsa_ftloc)
admin.site.register(Siterecs_samhsa_ftloc)
admin.site.register(Siterecs_samhsa_otp)
admin.site.register(Siterecs_dbhids_tad)
admin.site.register(Siterecs_other_srcs)
admin.site.register(Siterecs_hfp_fqhc)

# admin.site.register(Address)
# admin.site.register(Affiliate)
# admin.site.register(Email)
# admin.site.register(Licence)
# admin.site.register(Npi)
# admin.site.register(Phone)
# admin.site.register(ProvSiteRef)
# admin.site.register(Provider)
# admin.site.register(Site)
# admin.site.register(Xwaiver)






