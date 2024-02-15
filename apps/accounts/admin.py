from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import CustomUser, Customer



def active_members(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f"{res}کاربر فعال شدند"
    modeladmin.message_user(request, message)
def deactive_members(modeladmin, request, queryset):
    res = queryset.update(is_active = False)
    message = f"{res} کاربر غیر فعال شد"
    modeladmin.message_user(request, message)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("email","mobile_number","name","family","birth_date","is_admin","is_active",)
    list_filter = ("is_admin", "is_active")
    list_editable = ["is_active",]
    fieldsets = (
        (None,{"fields":("email", "password")}),
        ("اطلاعات شخصی", {"fields":("mobile_number","name","family","birth_date", "gender")}),
        ("دسترسی ها", {"fields":("is_active", "is_admin", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = ((None, {"fields":("email","mobile_number","name","family","birth_date", "password1","password2")}),)
    search_fields = ("email","mobile_number")
    ordering = ("is_admin","is_active",)
    filter_horizontal = ("groups", "user_permissions")
    actions = [active_members,deactive_members ]
        
    active_members.short_description = "فعال کردن کاربران"
    deactive_members.short_description = "غیرفعال کردن کاربران"
admin.site.register(CustomUser, CustomUserAdmin)

#--------------------------------------------------------------

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["user",]