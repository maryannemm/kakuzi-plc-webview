from django.urls import path
from .views import DashboardTemplateView, ProfileTemplateView, CartOrdersViews, UpdateOrderStatusView

app_name='finance'
urlpatterns = [
    path('', DashboardTemplateView.as_view(), name='dashboard'),
    path('profile', ProfileTemplateView.as_view(), name='profile'),
    path('orders', CartOrdersViews.as_view(), name='orders'),
    path('update-order/<int:order_id>', UpdateOrderStatusView.as_view(), name='update-order-status'),
]
