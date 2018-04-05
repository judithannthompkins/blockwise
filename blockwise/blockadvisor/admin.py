from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import Crime, Location, LocationInstance

admin.site.register(Crime)
admin.site.register(Location)
admin.site.register(LocationInstance)

