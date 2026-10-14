from django.contrib import admin
from .models import *

models = (
    Profile,
    Manager,
    Owner,
    Tenant
)

admin.site.register(models)