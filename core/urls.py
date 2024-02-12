from django.urls import path
from core.views import HomeTemplateView, PriceRangeFilterView, ShopListView, CategoryListView, SupplierListView, SingleSupplierDetailView,SingleProductDetailView, TagListView,AddReview,SearchView, CategoriesPriceRangeFilterView, AddToCartView, CartListView, CheckoutTemplateView
from core.views import DeleteFromCartView, UpdateCartView
app_name= 'core'
urlpatterns = [
    path("", HomeTemplateView.as_view(), name='index'),
    ####
    path("shop", ShopListView.as_view(), name='shop'),  
    path("shop/category/<str:cid>", CategoryListView.as_view(), name='category-list'), 
    path("shop/product-detail/<str:pid>", SingleProductDetailView.as_view(), name='product-detail'), 
    path("shop/product-detail/<str:pid>/review", AddReview.as_view(), name='add_review'),

    path('tag/<slug:tag_slug>/', TagListView.as_view(), name='tag-list'), 

    path('searchresults/', SearchView.as_view(), name='search-results'),
    path('shop/price_range_filter/', PriceRangeFilterView.as_view(), name='price-range-results'),
    path('category/price_range_filter/<str:cid>/', CategoriesPriceRangeFilterView.as_view(), name='category-price-range-results'),

    ##cart
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('<str:username>/cart', CartListView.as_view(), name='cart'),

    #updating cart
    path('<str:username>/cart/delete', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('<str:username>/cart/add', UpdateCartView.as_view(), name='update_cart'),

    #checkout
    path('cart/<str:username>/checkout', CheckoutTemplateView.as_view(), name='checkout'),
   

    ##### 
    path("vendor", SupplierListView.as_view(), name='vendor-list'),  
    path("vendor-detail/<str:vid>", SingleSupplierDetailView.as_view(), name='vendor-detail'),  
    
]  

