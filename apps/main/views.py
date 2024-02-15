from django.shortcuts import render
from django.conf import settings
from apps.products.models import ProductGroup
from django.db.models import Q
from django.views import View
from .models import Slider

from apps.products.models import ProductGroup, Product

def media_admin(request):
    return {"media_url": settings.MEDIA_URL}



def index(request):
    products_groups = ProductGroup.objects.filter(Q(is_active=True)& Q(group_parent=None))
    context = {
        "products_groups":products_groups
    }
    return render(request, 'main_app/index.html', context)

#------------------------------------------------------

class SliderView(View):
    def get(self, request):
        sliders = Slider.objects.filter(is_active = True)
        return render(request, "main_app/sliders.html", {"sliders":sliders})
    
#------------------------------------------------------
def handler404(request, exception=None):
    return render(request, "main_app/404.html")

#-----------------------------------------------------
