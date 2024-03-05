from django.db.models.base import Model as Model
from django.shortcuts import render, get_list_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView
from core.models import Feedback, CartOrder
from userauths.models import FinanceUserRole
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class DashboardTemplateView(TemplateView):
    template_name='finance_pages/dashboard.html'

    def get_context_data(self, **kwargs) -> dict[str, ]:
        context = super().get_context_data(**kwargs)
        context['pending_orders']=CartOrder.objects.filter(order_status='pending')
        context['completed_orders']=CartOrder.objects.filter(order_status='completed')
        context['shipped_orders']=CartOrder.objects.filter(order_status='shipped')
        context["latest_feedback"] = Feedback.objects.all().order_by('-id')[:4]
        return context

class ProfileTemplateView(LoginRequiredMixin,DetailView):
    model=FinanceUserRole
    template_name='finance_pages/profile.html'
    context_object_name='finance_manager'

    def get_object(self):
        return self.request.user.financeuserrole
    
class CartOrdersViews(TemplateView):
    template_name='finance_pages/orders.html'

    def get_context_data(self, **kwargs) -> dict[str, ]:
        context = super().get_context_data(**kwargs)
        context['pending_orders']=CartOrder.objects.filter(order_status='pending')
        context['completed_orders']=CartOrder.objects.filter(order_status='completed')
        context['shipped_orders']=CartOrder.objects.filter(order_status='shipped')
        context['delivered_orders']=CartOrder.objects.filter(order_status='delivered')
        return context
    
class UpdateOrderStatusView(UpdateView):
    model = CartOrder
    fields = ['order_status','payment_status']  
    template_name = 'finance_pages/update_order_status.html'  
    success_url=reverse_lazy('finance:orders')

    
    def get_object(self, queryset=None):
        order_id = self.kwargs.get('order_id')
        return CartOrder.objects.get(id=order_id)