from django.contrib import admin
from .models import (
    Salesperson,
    Client,
    ClientContact,
    VP,
    Vehicle,
    InternalTransport,
    OCFStock,
)

# Register your models here.
admin.site.register(Salesperson)
admin.site.register(Client)
admin.site.register(ClientContact)
admin.site.register(VP)
admin.site.register(Vehicle)
admin.site.register(InternalTransport)
admin.site.register(OCFStock)
