from django.contrib import admin
from .models import Warehause, WarehauseType


@admin.register(WarehauseType)
class WarehauseTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "ware_hause_type_title",)
    
@admin.register(Warehause)
class WarehauseAdmin(admin.ModelAdmin):
    list_display = ("product","qty","price","warehause_type","register_date",)
