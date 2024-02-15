from django.urls import path
from . import views

app_name="products"
urlpatterns = [
    path("categories/", views.get_products_groups, name="categories"),
    path("cheapest_products/", views.get_cheapest_products, name="cheapest_products"),
    path("latest_products/", views.get_latest_products, name="latest_products"),
    path("favorites_products/", views.get_favorites_products, name="favorites_products"),
    path("product_deatails/<slug:slug>/", views.ProductDeatailsView.as_view(), name="product_deatails"),
    path("related_products/<slug:slug>/", views.get_related_products, name="related_products"),
    path("products_groups/", views.ProductsGroupsView.as_view(), name="products_groups"),
    path("all_products/<slug:slug>/", views.ProductsView.as_view(), name="all_products"),
    path("brands_filter/<slug:slug>/", views.get_brands,name="brands_filter"),
    path("feature_filter/<slug:slug>/", views.get_feature_for_filter,name="feature_filter"),
    path("add_to_compare_list/", views.add_to_compare_list, name="add_to_compare_list"),
    path("delete_from_compare_list/", views.delete_from_compare_list, name="delete_from_compare_listt"),
    path("status_compare_list/", views.status_compare_list, name="status_compare_list"),
 

    path("ajax_admin/", views.filter_feature_value, name="filter_feature_value"),
   

]
