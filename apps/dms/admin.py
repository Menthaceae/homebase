from django.contrib import admin

from .models import *


models = (
    Message_Group,
    Message
)

admin.site.register(models)