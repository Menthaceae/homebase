from django.contrib import admin
from .models import *

models = (
    Profile
)

admin.site.register(models)