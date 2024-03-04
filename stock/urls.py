from django.urls import path
from .views import VendorrListView, SinglevendorDetailView, StockTemplateView, ProfileTemplateView, CategoryCreateView, CategoryUpdateView, VendorCreateView , VendorUpdateView, ProductCreateview, ProductUpdateView, ProductListView, CategoryListView


app_name='stock'
urlpatterns = [
    ##### 
    path('',StockTemplateView.as_view(), name='dashboard'),
    path("vendor-list", VendorrListView.as_view(), name='vendor-list'),  
    path("vendor-detail/<str:username>", SinglevendorDetailView.as_view(), name='vendor-detail'),  
    path('profile', ProfileTemplateView.as_view(), name='profile'),
    path('category-create', CategoryCreateView.as_view(), name='create-category'),
    path('update-category/<str:cid>', CategoryUpdateView.as_view(), name='update-category'),
    path('vendor-create', VendorCreateView.as_view(), name='create-vendor'),
    path('vendor-update/<str:username>', VendorUpdateView.as_view(), name='update-vendor'),
    path('create-product', ProductCreateview.as_view(), name='create-product'),
    path('update-product/<str:pid>', ProductUpdateView.as_view(), name='product-update'),
    path('product-list', ProductListView.as_view(), name='product-list'),
    path('category-list', CategoryListView.as_view(), name='category-list'),



]
