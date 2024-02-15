from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, ProductGroup,FeatureValue,Brand
from django.db.models import Q, Count, Min, Max, Avg
from django.views import View
from .filters import ProductFilter
from django.core.paginator import Paginator
from .compare import CompareProduct
from django.http import HttpResponse
from apps.scoring_favorite.models import Scoring
#-------------------------------------------------------------------------
#اسلایدر متحرک  گروه های محصولات محصولات
def get_products_groups(request, *args, **kwargs):
    products_groups = ProductGroup.objects.filter(Q(is_active=True)& Q(group_parent=None))[:10]
    context = {
        "products_groups":products_groups
    }
    return render(request, "products_app/partials/categories.html", context)
#-------------------------------------------------------------------------

#ارزانترین محصولات
def get_cheapest_products(request, *args, **kwargs):
    products = Product.objects.filter(is_active=True).order_by('-price')[:8]
    return render(request, "products_app/partials/cheapest_products.html", {"products":products,})
#-------------------------------------------------------------------------

#جدیدترین محصولات فروشگاه

def get_latest_products(request, *args, **kwargs):
    products = Product.objects.filter(is_active=True).order_by('-published_date')[:6]
    return render(request, "products_app/partials/latest_products.html", {"products":products,})
#-------------------------------------------------------------------------
def get_favorites_products(request, *args, **kwargs):
    products=Product.objects.annotate(avg_score=Avg('scoring_product__score')).order_by('-avg_score')[:6]
    return render(request, "products_app/partials/favorites_products.html", {"products":products,})
#-------------------------------------------------------------------------
#جزییات محصول

class ProductDeatailsView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        if product.is_active:
            return render(request, "products_app/product_deatails.html",{"product":product})
    
#-------------------------------------------------------------------------
# محصولات مرتبط
def get_related_products(request, *args, **kwargs):
    current_product = get_object_or_404(Product, slug = kwargs["slug"])
    related_products = []
    for group in current_product.product_group.all():
        related_products.extend(Product.objects.filter(Q(is_active=True)& Q(product_group=group)& ~Q(id=current_product.id)))

    return render(request, "products_app/partials/related_products.html", {"related_products":related_products,})

#-------------------------------------------------------------------------
#نمایش تمام گروه های کالاها
class ProductsGroupsView(View):
    def  get(self, request, *args, **kwargs):
        groups = ProductGroup.objects.filter(Q(is_active=True)& Q(group_parent=None))
        groups = groups.annotate(count =Count("products_of_groups"))
        return render(request, "products_app/products_groups.html",{"groups":groups})
#-------------------------------------------------------------------------
#همه محصولات هر گروه
class ProductsView(View):
    def get(self, request, *args, **kwargs):
        current_group = get_object_or_404(ProductGroup, slug=kwargs["slug"])
        all_products = Product.objects.filter(is_active=True)
        products = Product.objects.filter(Q(is_active=True)& Q(product_group=current_group))
        groups = ProductGroup.objects.filter(Q(is_active=True)& ~Q(group_parent=None))[:10]
        min_max_price = products.aggregate(min = Min("price"), max = Max("price"))

        #فیلتر بر اساس قیمت
        price_filter = ProductFilter(request.GET, queryset=products)
        products= price_filter.qs
        #فیلتر بر اساس برند کالا
        brands_filter = request.GET.getlist("brand")
        if brands_filter:
            products = products.filter(product_brand__id__in=brands_filter)

        #فیلتر بر اساس ویژگی ها
        features_filter = request.GET.getlist("feature")
        if features_filter:
            products = products.filter(features_of_product__filter_value__id__in=features_filter).distinct()

        sort_type = request.GET.get("sort_type")
        if not sort_type:
            sort_type="0"
        if sort_type == "1":
            products= products.order_by("price")
        elif sort_type=="2":
            products=products.order_by("-price")
        
        #paginator
        products_per_page = 1
        paginator = Paginator(products, products_per_page)
        page_number = request.GET.get("page")  
        page_obj = paginator.get_page(page_number) 
        product_count = products.count()   
       

        context = {
            "all_products":all_products,
            "products":products, 
            "groups":groups,
            "min_max_price":min_max_price,
            "current_group":current_group,
            "page_obj":page_obj,
            "price_filter":price_filter,
            "product_count":product_count ,
            "sort_type":sort_type,
        }
        return render(request, "products_app/all_products.html",context)
#-------------------------------------------------------------------------
def get_brands(request, *args, **kwargs):
    current_group = get_object_or_404(ProductGroup, slug=kwargs["slug"]) 
    brand_list_id = current_group.products_of_groups.filter(is_active=True).values("product_brand_id")
    brands = Brand.objects.filter(pk__in=brand_list_id ).annotate(count=Count("product_of_brands"))\
                                                        .filter(~Q(count=0)).order_by("-count")
    return render(request, "products_app/partials/brand_filter.html",{"brands":brands})

#-------------------------------------------------------------------------
#فیلتر بر اساس ویژگی ها
def get_feature_for_filter(request, *args, **kwargs):
    product_group = get_object_or_404(ProductGroup, slug=kwargs["slug"])
    brand_list_id = product_group.products_of_groups.filter(is_active=True).values("product_brand_id")
    brands = Brand.objects.filter(pk__in=brand_list_id ).annotate(count=Count("product_of_brands"))\
                                                        .filter(~Q(count=0)).order_by("-count")
    feature_list = product_group.features_of_product_group.all()
    feature_dict = dict()
    for feature in feature_list:
        feature_dict[feature] = feature.feature_values.all()
    return render(request,"products_app/partials/feature_filter.html", {"feature_dict":feature_dict, "brands":brands})

#-------------------------------------------------------------------------
#تابع انتخاب مقادیر ویزگی ها مربوط به پنل ادمین
def filter_feature_value(request):
     if request.method == "GET":
        feature_id = request.GET["feature_id"]
        feature_values = FeatureValue.objects.filter(feature_id=feature_id)
        res = {fv.value_title:fv.id for fv in feature_values}
        return JsonResponse(data=res, safe=False)

#-------------------------------------------------------------------------
#مقایسه محصولات
#صفحه اصلی مقایسه کالاها
class ShowCompareListView(View):
    def get(self, request, *args, **kwargs):
        compare_list = CompareProduct(request)
        return render(request, "products_app/compare_list.html", {"compare_list":compare_list})
    
#-------------------------------------------------------------------------
#نمایش جدول مقایسه

def compare_table(request):
    compareList = CompareProduct(request)
    products = []
    for productId in compareList.compare_product:
        product = Product.objects.get(id=productId)
        products.append(product)

    features = []
    for product in products:
        for item in product.features_of_product.all():
            if item.feature not in features:
                features.append(item.feature)

    context = {
        "products" : products,
        "features" : features
    }
    return render(request, "products_app/partials/compare_table.html", context)

#-------------------------------------------------------------------------
#تعداد کالای موجود در لیست مقایسه
def status_compare_list(request):
    compareList = CompareProduct(request)
    return HttpResponse(compareList.count)
#-------------------------------------------------------------------------
#اضافه کردن به لیست مقایسه
def add_to_compare_list(request):
    productId = request.GET.get("productId")
    compareList = CompareProduct(request)
    compareList.add_to_compare_product(productId)
    return HttpResponse("کالا به لیست مقایسه افزوده شد")

#-------------------------------------------------------------------------
#حذف از لیست مقایسه
def delete_from_compare_list(request):
    productId = request.GET.get("productId")
    compareList = CompareProduct(request)
    compareList.delete_from_compare_product(productId)
    return redirect("products:compare_table")




