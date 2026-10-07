from django.contrib import admin
from .models import *

models = (
    Manager,
    Homebase,
    SubProperty,
    OwnedProperty,
    Owner,
    Rental,
    Tenant,
)

admin.site.register(models)