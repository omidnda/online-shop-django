from django.shortcuts import render
from apps.products.models import Product
from .models import Scoring, Favorite
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.views import View
from django.db.models import Count
def add_score(request):
    productId = request.GET.get("productId")
    score = request.GET.get("score")

    product = Product.objects.get(id=productId)
    Scoring.objects.create(
        product = product,
        scoring_user = request.user,
        score = score
    )
    return HttpResponse("امتیاز شما با موفقیت ثبت شد")
#------------------------------------------------------------
def set_cookie(request):
    response = render(request, "")
    response.set_cookie(key="supermarket", value="")

#------------------------------------------------------------
def add_to_favorite(request):
    productId = request.GET.get("productId")
    product = Product.objects.get(id=productId)
    flag=Favorite.objects.filter(
        Q(user_id=request.user.id) &
        Q(product_id = productId)
    ).exists()

    if not flag:
        Favorite.objects.create(
            product=product,
            user = request.user
        )
        return HttpResponse("این کالا به لیست علاقه مندی های شما اضافه شد")
    return HttpResponse("این کالا از قبل در لیست شما قرار دارد")


 # product = Product.objects.get(id=product_id)
    # favorites_list = request.COOKIES.get('favorites_list', '').split(',')
    
    # if str(product.id) not in favorites_list:
    #     favorites_list.append(str(product.id))
    
    # response = JsonResponse({'message': "این کالا به لیست علاقه مندی های شما اضافه شد"})
    # response.set_cookie('favorites_list', ','.join(favorites_list))
    # return response
#---------------------------------------------------------
#نمایش لیست کالاهای مورد علاقه

class UserfavoritView(View):
    def get(self, request, *args, **kwargs):
        favorit_product_user = Favorite.objects.filter(Q(user_id=request.user.id))
        return render(request, "scoring_favorite_apps/favorit_user.html", {"favorit_product_user":favorit_product_user})