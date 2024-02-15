from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


app_name = 'main'
urlpatterns = [
    path('', views.index, name="index"),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'))),
    path('sliders/', views.SliderView.as_view(), name="sliders"),

]
