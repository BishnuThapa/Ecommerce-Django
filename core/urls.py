from django.urls import path
from . import views

#namespacing urls
app_name='core'
urlpatterns = [
    path('', views.index, name='index'),

    # PRODUCTS
    path('products/', views.product_list_view, name='product-list'),

    # CATEGORIES
    path('category/', views.category_list_view, name='category-list'),
    path('category/<cid>', views.category_product_list,
         name='category-product-list'),

    # VENDOR
    path('vendor/', views.vendor_list_view, name='vendor-list'),
    path('vendor/<vid>', views.vendor_detail_view, name='vendor-detail'),
]
