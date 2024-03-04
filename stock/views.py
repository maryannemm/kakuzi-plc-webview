from django.shortcuts import render
from userauths.models import StockUserRole
from django.views.generic import TemplateView,DetailView,ListView,CreateView,UpdateView
from userauths.models import VendorUser
from core.models import Feedback,Product,Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import CreateProductForm
from django.urls import reverse_lazy


# Create your views here.
class StockTemplateView(TemplateView):
    template_name = "stock_pages/dashboard.html"

    def get_context_data(self, **kwargs) -> dict[str, ]:
        context = super().get_context_data(**kwargs)
        context["feedbacks"] =  Feedback.objects.all().order_by('-id')[:3]
        context['latest_products']=Product.objects.all().order_by('-id')[:3]
        context['vendors_unapproved']= VendorUser.objects.filter(verified=False)[:4]
        return context    

class VendorrListView(LoginRequiredMixin, ListView):
    model=VendorUser
    template_name='stock_pages/vendor_list.html'
    paginate_by=10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vendors"] = VendorUser.objects.all()
        return context
    
class SinglevendorDetailView(LoginRequiredMixin, DetailView):
    model=VendorUser
    template_name=  'stock_pages/vendor-detail.html '
    context_object_name = 'vendor'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(VendorUser,username=username)
    
class ProductListView(ListView):
    template_name = 'stock_pages/product-list.html'
    model=Product
    paginate_by=10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products']=Product.objects.all().order_by('-id')
        context['categories']=Category.objects.all().order_by('-id')
       
        
        return context

class ProductCreateview(CreateView):
    model=Product
    template_name='stock_pages/create-product.html'
    fields=['title', 'image', 'description', 'price', 'quantity_available', 'is_available', 'tags', 'product_status', 'featured', 'user', 'vendor', 'category', 'life', 'mfd']
    success_url = reverse_lazy('stock:product-list') 

class ProductUpdateView(UpdateView):
    model=Product
    fields=['title', 'image', 'description', 'price', 'quantity_available', 'is_available', 'tags', 'product_status', 'featured', 'life', 'mfd']
    template_name='stock_pages/product_update.html'
    success_url=reverse_lazy('stock:product-list')

    def get_object(self, queryset=None):
        pid = self.kwargs.get('pid')
        return get_object_or_404(Product, pid=pid)

class CategoryCreateView(CreateView):
    model=Category
    template_name='stock_pages/create-category.html'
    fields=['image', 'title']
    success_url = reverse_lazy('stock:category-list') 

class CategoryUpdateView(UpdateView):
    model=Category
    fields=['image', 'title']
    template_name='stock_pages/category_update.html'
    success_url=reverse_lazy('stock:category-list')

    def get_object(self, queryset=None):
        cid = self.kwargs.get('cid')
        return get_object_or_404(Category, cid=cid)

class VendorCreateView(CreateView):
    model=VendorUser
    template_name='stock_pages/create-vendor.html'
    fields=['username','password','email','phone','full_name','verified','phone','image','title', 'vendor_address', 'description', 'city', 'business_email','country' ]
    success_url = reverse_lazy('stock:vendor-list') 

class VendorUpdateView(UpdateView):
    model=VendorUser
    fields=['verified','phone','image','title', 'vendor_address', 'description', 'city', 'business_email','country' ]
    template_name='stock_pages/vendor_update.html'
    success_url=reverse_lazy('stock:vendor-list')

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(VendorUser, username=username)

class ProfileTemplateView(TemplateView):
    template_name='stock_pages/profile.html'
    model=StockUserRole
    
    def get_context_data(self, **kwargs) -> dict[str, ]:
        context = super().get_context_data(**kwargs)
        context["stock_manager"] = get_object_or_404(StockUserRole, email=self.request.user.email)
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'stock_pages/category-list.html'
    paginate_by=10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category =Category.objects.all()
        context['category'] = category
        return context 
