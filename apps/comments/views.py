from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import CommentForm
from apps.products.models import Product
from .models import Comment
from django.contrib import messages
from apps.accounts.models import Customer
class CommentView(View):
    def get(self, request, *args, **kwargs):
        productId = request.GET.get("productId")
        commentId = request.GET.get("commentId")
        slug = kwargs["slug"]
        initial_dict = {
            "product_id" : productId,
            "comment_id" : commentId
        }
        form = CommentForm(initial=initial_dict)
        return render(request,"comments_app/create_comment.html", {"form":form, "slug":slug} )
    
    def post(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            product = get_object_or_404(Product, slug=slug)
            parent = None
            if cd["comment_id"]:
                parentId = cd["comment_id"]
                parent = Comment.objects.get(id=parentId)

            Comment.objects.create(
                product=product,
                user1 = get_object_or_404(Customer, user= request.user),
                comment = cd["comment_text"],
                comment_parent = parent
            )
            messages.success(request, "دیدگاه شما ارسال شد", "success")
            return redirect("products:product_deatails", product.slug)
        messages.error(request, "خطا در ارسال", "danger")
        return redirect("products:product_deatails", product.slug)