from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test_api),
    path('test_post', views.test_api_post),
    path('store_image', views.store_image),
]