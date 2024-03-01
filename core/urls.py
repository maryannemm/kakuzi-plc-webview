from django.urls import path, include
from core.views import *
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
    
    #paypal urls
    path('paypal/', include("paypal.standard.ipn.urls")),
    path('paypal-ipn/', csrf_exempt(paypal_ipn_views.ipn), name='paypal-ipn'),
    path('paypal/completed/', PayPalSuccessView.as_view(), name='paypal_success'),
    path('paypal/cancel/', PayPalCancelView.as_view(), name='paypal_cancel'),
    path('paypal/error/', PayPalErrorView.as_view(), name='paypal_error'),

    #customer dashboard
    path('<str:username>/dashboard', CustomerDashboardTemplateView.as_view(), name='customer-dashboard'),
    path('<str:username>/order', CustomerOrdersListView.as_view(), name='customer-orders'),
    path('<str:username>/order/<int:order_id>/', CustomerOrderDetailView.as_view(), name='order-detail'),
    path('<str:username>/address/', CustomerAddressTemplateView.as_view(), name='customer-address'),

    #edit customer address
    path('address/edit/<int:address>', CustomerEditAddressUpdateView.as_view(), name= 'edit-address' ),
    path('address/delete/<int:pk>', CustomerAddressDeleteView.as_view(), name= 'delete-address' ),
    path('address/default/<int:pk>', CustomerDefaultAddressUpdateView.as_view(), name= 'make-default-address' ),
    path('create-address/', CustomerCreatetAddressUpdateView.as_view(), name= 'create-address' ),

    # wishlist
    path('add-to-wishlist/', AddWishlistView.as_view() ,name='add-to-wishlist'),
    path('wish-list/<str:username>', WishListListView.as_view() ,name='wishlist'),
    path('wishlist/delete/<str:pid>/', WishlistItemDeleteView.as_view(), name='wishlist-delete'),

    #about us+ contact us
    path('about-us/', AboutUsTemplateView.as_view(), name='about'),
    path('contact-us/', ContactUsView.as_view(), name='contact'),
   
   #customer profile
   path('<str:username>/edit-profile/', EditCustomerProfileView.as_view(), name='edit-profile'),

   #feedback
    path('<str:username>/feedback', CustomerFeedbackFormView.as_view(),name='feedback'),

    ##### 
    path("vendor", SupplierListView.as_view(), name='vendor-list'),  
    path("vendor-detail/<str:vid>", SingleSupplierDetailView.as_view(), name='vendor-detail'),  
    
]  

