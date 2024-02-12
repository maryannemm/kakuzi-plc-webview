from django.urls import path
from . import views


app_name='userauths'
urlpatterns = [
    path('sign-up/',views.RegisterView.as_view(), name='sign-up'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
]
