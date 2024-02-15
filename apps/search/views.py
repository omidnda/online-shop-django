from django.shortcuts import render, redirect
from django.db.models import Q
from django.views import View
from apps.products.models import Product

class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")
        products = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(description__icontains=query)
        )
        context = {"products":products}
        return render(request, "search_apps/search_results.html", context)