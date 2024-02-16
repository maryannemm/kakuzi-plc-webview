from django.urls import path, include
from core.views import HomeTemplateView, PriceRangeFilterView, ShopListView, CategoryListView, SupplierListView, SingleSupplierDetailView,SingleProductDetailView, TagListView,AddReview,SearchView, CategoriesPriceRangeFilterView, AddToCartView, CartListView, CheckoutTemplateView
from core.views import DeleteFromCartView, UpdateCartView, PayPalSuccessView, PayPalCancelView, PayPalErrorView
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.ipn import views as paypal_ipn_views
app_name= 'core'
urlpatterns = [
    path("", HomeTemplateView.as_view(), name='index'),

    #### products urls
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

    # invoice
    path('<str:username>/invoice', PayPalSuccessView.as_view(), name='invoice'),
    
    #paypa urls
    path('paypal/', include("paypal.standard.ipn.urls")),
    path('paypal-ipn/', csrf_exempt(paypal_ipn_views.ipn), name='paypal-ipn'),
    path('paypal/completed/', PayPalSuccessView.as_view(), name='paypal_success'),
    path('paypal/cancel/', PayPalCancelView.as_view(), name='paypal_cancel'),
    path('paypal/error/', PayPalErrorView.as_view(), name='paypal_error'),
   

    ##### 
    path("vendor", SupplierListView.as_view(), name='vendor-list'),  
    path("vendor-detail/<str:vid>", SingleSupplierDetailView.as_view(), name='vendor-detail'),  
    
]  

