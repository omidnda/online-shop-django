"""
URL configuration for supermarket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls', namespace='main'), name='main'),
    path('accounts/', include('apps.accounts.urls', namespace='accounts'), name='accounts'),
    path('products/', include('apps.products.urls', namespace='products'), name='products'),
    path('orders/', include('apps.orders.urls', namespace='orders'), name='orders'),
    path('discount/', include('apps.discount.urls', namespace='discount'), name='discount'),
    path('payments/', include('apps.payments.urls', namespace='payments'), name='payments'),
    path('comments/', include('apps.comments.urls', namespace='comments'), name='comments'),
    path('warehauses/', include('apps.warehauses.urls', namespace='warehauses'), name='warehauses'),
    path('scoring_favorite/', include('apps.scoring_favorite.urls', namespace='scoring_favorite'), name='scoring_favorite'),
    path('search/', include('apps.search.urls', namespace='search'), name='search'),
    path('blog/', include('apps.blog.urls', namespace='blog'), name='blog'),
    path('ckeditor',include('ckeditor_uploader.urls')),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
admin.site.site_header = "پنل مدیریت"
#admin.site.index_title = ""  scoring_faivorit

handler404 = "apps.main.views.handler404"