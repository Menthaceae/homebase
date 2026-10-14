from django.contrib import admin
from .models import *

models = (
    Homebase,
    SubProperty,
    OwnedProperty,
    Rental,
)

admin.site.register(models)