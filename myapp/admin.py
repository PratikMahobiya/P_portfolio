from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Contact_form_model)
class Contact_admin(admin.ModelAdmin):
    list_display = ('U_id','Name','Email','Contact','Message','Date','File_status')
    list_per_page = 10
    search_fields = ['Name','Contact']

@admin.register(models.File_model)
class File_admin(admin.ModelAdmin):
    list_display = ('U','File')
    list_per_page = 10