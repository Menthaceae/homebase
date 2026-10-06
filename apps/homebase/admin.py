from django.contrib import admin
from .models import *

models = (
    PropertyManager,
    Homebase,
    SubProperty,
    PropertyOwner,
    Rental,
    Tenant
)

admin.site.register(models)