from typing import Any, Optional
from django.contrib import admin
from django.db.models.fields.related import ManyToManyField
from django.db.models.query import QuerySet
from django.forms.models import ModelMultipleChoiceField
from django.http.request import HttpRequest
from .models import Brand, ProductGroup, Product, ProductFeature, ProductImageGallery, Feature,FeatureValue
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from django.db.models.aggregates import Count



@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["brand_name", "slug", "is_active"]
    list_filter = ["brand_name"]
    ordering = ["brand_name"]
    search_fields = ["brand_name"]

#------------------------------------------------------------------  
def deactive_groups(modeladmin, request, queryset):
    res = queryset.update(is_active = False)
    message = f"{res} گروه کالا غیرفعال شد"
    modeladmin.message_user(request,message)
def active_groups(modeladmin, request, queryset):
    res = queryset.update(is_active = True)
    message = f"{res} گروه فعال شد"
    modeladmin.message_user(request, message)
class ProductGroupInline(admin.TabularInline):
    model = ProductGroup
    extra = 1


class GroupFilter(admin.SimpleListFilter):
    title = "گروه محصولات"
    parameter_name = "group"

    def lookups(self, request, model_admin):
        sub_groups = ProductGroup.objects.filter(~Q(group_parent=None))
        groups = set([item.group_parent for item in sub_groups])
        return [(group.id, group.group_name) for group in groups]

    def queryset(self, request, queryset):
        if self.value() != None:            
            return queryset.filter(Q(group_parent=self.value()))
        return queryset
    

@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ["group_name", "group_parent","count_product_of_group" ,"register_date", "update_date", "published_date", "is_active"]
    list_filter = [GroupFilter]
    ordering = ["group_parent","group_name"]
    search_fields = ["group_name"]
    inlines = [ProductGroupInline]
    actions = [deactive_groups,active_groups]
    list_editable=["is_active"]

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductGroupAdmin, self).get_queryset(*args, **kwargs)
        qs = qs.annotate(product_of_group=Count("products_of_groups"))
        return qs

    def count_product_of_group(self, obj):
        return obj.product_of_group
    
    deactive_groups.short_description = "غیرفعال کردن گروه های انتخابی"
    active_groups.short_description = "فعال کردن گروه های انتخابی"
    count_product_of_group.short_description = "تعداد کالای هر گروه"
#------------------------------------------------------------------  
class FeatureValueInline(admin.TabularInline):
    model = FeatureValue
    extra =3

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ["feature_name"]
    list_filter = ["feature_name",]
    ordering = ["feature_name",]
    search_fields = ["feature_name"]
    inlines=[FeatureValueInline]
#------------------------------------------------------------------

def deactive_product(modeladmin, request, queryset):
    res = queryset.update(is_active= False)
    message = f"{res} کالا غیرفعال شد"
    modeladmin.message_user(request,message)

def active_product(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f"{res} کالا فعال شد"
    modeladmin.message_user(request, message)


   
class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 3 
    class Media:
        js = (
            # 'vendor/jquery-3.3.1/jquery.min.js',
            #'vendor/bootstrap-4.5.3/js/bootstrap.bundle.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.0/jquery.min.js',
            'js/admin_script.js/',
        )

class ProductImageGalleryInline(admin.TabularInline):
    model = ProductImageGallery
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["product_name","product_brand","display_product_groups","price","update_date","is_active","slug",]
    list_filter = ["product_brand",]
    ordering = ["update_date","product_name"]
    search_fields = ["product_name"]
    actions = [deactive_product, active_product]
    inlines = [ProductFeatureInline, ProductImageGalleryInline]

    def display_product_groups(self, obj):
        return ', '.join([group.group_name for group in obj.product_group.all()])
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        print(kwargs)
        if db_field.name == "product_group":
            kwargs["queryset"] = ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    deactive_product.short_description = "غیرفعال کردن کالاهای انتخابی"
    active_product.short_description = "فعال کردن کالاهای انتخابی"
    display_product_groups.short_description = "گروه های کالا"


#------------------------------------------------------------------
#    
# class ProductFeatureInline(admin.TabularInline):
#     model = ProductFeature
#     extra = 3 

# class ProductImageGalleryInline(admin.TabularInline):
#     model = ProductImageGallery
#     extra = 3


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ["product_name", "price", "product_group ", "product_brand", "slug", "is_active"]
#     inlines = [ProductFeatureInline, ProductImageGallery]

