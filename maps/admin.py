from django.contrib import admin
from .models import Map

# Register your models here.
class MapAdmin(admin.ModelAdmin):
    fields = "__all__"


admin.site.register(Map, MapAdmin)