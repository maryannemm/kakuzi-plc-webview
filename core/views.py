from typing import Any
from urllib import request, response
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from taggit.models import Tag
from django.db.models import Count,Avg,Q, Sum
from core.forms import ProductReviewForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils import timezone




from .models import Category, Supplier, Product, ProductImages, CartOrder, CartOrderItems, ProductReview, WishList, Address

# Create your views here.
class HomeTemplateView(TemplateView):
    template_name = "customer_pages/index.html"
    

class ShopListView(ListView):
    template_name = 'customer_pages/shop.html'
    model=Product
    paginate_by=10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products']=Product.objects.all().order_by('-id')
        context['categories']=Category.objects.all().order_by('-id')
       
        
        return context
class CategoryListView(ListView):
    model = Category
    template_name = 'customer_pages/category.html'
    paginate_by=10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, cid=self.kwargs['cid'])
        context['category'] = category
        context['products'] = Product.objects.filter(product_status='published', category=category).order_by('-id')
        return context
    
class SupplierListView(LoginRequiredMixin, ListView):
    model=Supplier
    template_name='stock_pages/vendor_list.html'
    paginate_by=10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vendors"] = Supplier.objects.all()
        return context
    

class SingleSupplierDetailView(LoginRequiredMixin, DetailView):
    model=Supplier
    template_name=  'stock_pages/vendor-detail.html '
    context_object_name = 'vendor'

    def get_object(self, queryset=None):
        # Use get_object_or_404 to get the Supplier based on vid
        return get_object_or_404(Supplier, vid=self.kwargs['vid'])

class SingleProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'customer_pages/product-detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        return get_object_or_404(Product, pid=self.kwargs['pid'])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pid=self.kwargs['pid'])
        # Dynamically set product availability based on quantity_available
        product.is_available = product.quantity_available > 0

        context['reviews'] = ProductReview.objects.filter(product=product).order_by('-date')
        context['average'] = ProductReview.objects.filter(product=product).aggregate(rating=Avg('ratings'))
        context['product'] = product

        # Add the AddReviewForm and AddReview view
        context['add_review_form'] = ProductReviewForm()
        context['add_review_view'] = AddReview.as_view()

        context['user_reviewed'] = product.user_reviewed
        
        # Include the pid in the context
        context['pid'] =self.kwargs['pid'] 

        return context


class TagListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'customer_pages/tag-list.html'  # Set your actual template name
    context_object_name = 'products'
    paginate_by = 9
    
    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        tag = Tag.objects.get(slug=tag_slug)
        return Product.objects.filter(tags=tag, product_status="published")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        context['tag'] = Tag.objects.get(slug=tag_slug)
        return context
    

@method_decorator(login_required, name='dispatch')
class AddReview(CreateView):
    model = ProductReview
    form_class = ProductReviewForm
    template_name = 'customer_pages/product-detail.html'

    def get_product_id(self):
        return self.kwargs.get('pid')

    def form_valid(self, form):
        pid = self.get_product_id()
        product = get_object_or_404(Product, pid=pid)

        # Check if the user has already reviewed
        if ProductReview.objects.filter(product=product, user=self.request.user).exists():
            messages.warning(self.request, 'You already reviewed this product.', extra_tags='custom-alert-danger')
            product.user_reviewed = True
            return redirect('core:product-detail', pid=pid)
        else:
            product.user_reviewed = False

        form.instance.product = product
        form.instance.user = self.request.user

        response = super().form_valid(form)

        # Check if the review was successfully saved
        if response.status_code == 302:
            messages.success(self.request, 'Review submitted successfully.')
            product.user_reviewed = True

        return response

    def get_success_url(self):
        pid = self.get_product_id()
        return reverse('core:product-detail', args=[pid])

class SearchView(View):
    template_name = 'core/search_results.html' 

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')

        if query:
            # Use Q objects for a case-insensitive search across multiple fields
            results = Product.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__title__icontains=query)
            ).distinct()

            context = {'results': results, 'query': query}
        else:
            context = {}

        return render(request, self.template_name, context)
    
class PriceRangeFilterView(TemplateView):
    template_name = 'core/price-range-slider-results.html'

    def get(self, request, *args, **kwargs):
        # Handle form submission and filter products based on the selected price range
        min_price =10
        
        max_price = int(request.GET.get('price_range', 0))

        filtered_products = Product.objects.filter(price__gte=min_price, price__lte=max_price)

        context = {
            'min_price': min_price,
            'max_price': max_price,
            'filtered_products': filtered_products,
        }

        return self.render_to_response(context)

class CategoriesPriceRangeFilterView(TemplateView):
    template_name = 'core/price-range-slider-results.html'

    def get(self, request, *args, **kwargs):
        # Handle form submission and filter products based on the selected price range
        min_price = 10
        max_price = int(request.GET.get('price_range', 0))
        category = get_object_or_404(Category, cid=self.kwargs['cid'])

        filtered_products = Product.objects.filter(category=category, price__gte=min_price, price__lte=max_price)

        context = {
            'min_price': min_price,
            'max_price': max_price,
            'filtered_products': filtered_products,
        }

        return self.render_to_response(context)




class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        # Retrieve data from the POST request
        pid = request.POST.get('pid')
        title = request.POST.get('title')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        image = request.POST.get('image')

        # Check if the cart order exists in the session
        if 'cart_order' in request.session:
            cart_order = request.session['cart_order']
        else:
            # If the cart order doesn't exist, create a new one
            cart_order = {'items': []}

        # Update or add the item to the cart
        updated_item = False
        for item in cart_order['items']:
            if item['pid'] == pid:
                item['quantity'] += int(quantity)
                updated_item = True
                break

        if not updated_item:
            cart_order['items'].append({
                'pid': pid,
                'title': title,
                'price': price,
                'quantity': int(quantity),
                'image': image,
            })

        # Update the cart order in session
        request.session['cart_order'] = cart_order

        # Calculate the total number of items in the cart
        total_items = sum(item['quantity'] for item in cart_order['items'])

        # Update the cart count in session
        request.session['cart_count'] = total_items

        # Calculate the total price of the cart
        total_price = sum(float(item['price']) * item['quantity'] for item in cart_order['items'])

        # Show a success message
        messages.success(request, 'Product added to cart successfully')

        # Save cart data to the database
        if request.user.is_authenticated:
            cart_order_obj = CartOrder.objects.create(
                user=request.user,
                price=total_price,
                payment_status=False,
                order_date=timezone.now(),
                order_status='processing'
            )
            for item in cart_order['items']:
                CartOrderItems.objects.create(
                    order=cart_order_obj,
                    item=item['title'],
                    image=item['image'],
                    price=item['price'],
                    total=float(item['price']) * item['quantity'],
                    qty=item['quantity']
                )

        # Return a JSON response with the success message and total number of items
        return JsonResponse({
            'message': 'Product added to cart successfully',
            'total_items': total_items,
            'total_price': total_price,
            'cart_items': cart_order['items'],
            'image': image   
        })

    
class CartListView(LoginRequiredMixin, TemplateView):
    template_name = 'customer_pages/cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve cart order items from the session
        cart_order_items = self.request.session.get('cart_order', {}).get('items', [])
        
        # Initialize total items and total price
        total_items = sum(item['quantity'] for item in cart_order_items)
        total_price = sum(float(item['price']) * int(item['quantity']) for item in cart_order_items)+200
        
        # Retrieve full product details for each item in the cart
        cart_items_details = []
        for item in cart_order_items:
            product = get_object_or_404(Product, pid=item['pid'])
            cart_items_details.append({
                'product': product,
                'quantity': item['quantity'],
                'total': float(item['price']) * int(item['quantity']),
            })
        
        # Add cart items, total items, and total price to the context
        context['cart_items'] = cart_items_details
        context['total_items'] = total_items
        context['total_price'] = total_price
        context['cart_order_items']=cart_order_items

        self.request.session.save()
        
        
        return context
    
class DeleteFromCartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pid = request.GET.get('pid')
        if 'cart_order' in request.session:
            cart_order = request.session['cart_order']
            for item in cart_order['items']:
                if item['pid'] == pid:
                    cart_order['items'].remove(item)
                    break
            request.session['cart_order'] = cart_order
            
        return HttpResponseRedirect(reverse('core:cart', args=[request.user.username]))

    def post(self, request, *args, **kwargs):
        pid = request.POST.get('pid')

        # Check if the cart order exists in the session
        if 'cart_order' in request.session:
            cart_order = request.session['cart_order']
        else:
            return JsonResponse({'error': 'Cart not found'}, status=400)

        # Remove the specified item from the cart
        for item in cart_order['items']:
            if item['pid'] == pid:
                cart_order['items'].remove(item)
                break

        # Update the cart order in session
        request.session['cart_order'] = cart_order

        # Calculate the total number of items in the cart
        total_items = sum(item['quantity'] for item in cart_order['items'])

        # Calculate the total price of the cart
        total_price = sum(float(item['price']) * item['quantity'] for item in cart_order['items'])

        # Update the cart count in session
        request.session['cart_count'] = total_items 

        # Return a JSON response with the total price of the cart
        return JsonResponse({'total_price': total_price})


class UpdateCartView(LoginRequiredMixin, View):
   def post(self, request, *args, **kwargs):
        pid = request.POST.get('pid')
        quantity = int(request.POST.get('quantity'))

        # Check if the cart order exists in the session
        if 'cart_order' in request.session:
            cart_order = request.session['cart_order']
        else:
            return JsonResponse({'error': 'Cart not found'}, status=400)

        # Update the quantity of the specified item in the cart
        for item in cart_order['items']:
            if item['pid'] == pid:
                item['quantity'] = quantity
                break

        # Update the cart order in session
        request.session['cart_order'] = cart_order

        # Calculate the total number of items in the cart
        total_items = sum(item['quantity'] for item in cart_order['items'])

        # Calculate the total price of the cart
        total_price = sum(float(item['price']) * item['quantity'] for item in cart_order['items'])

        # Update the cart count in session
        request.session['cart_count'] = total_items
         

        # Return a JSON response with the total price of the cart
        return JsonResponse({'total_price': total_price})
        
       
    # Return your HTTP response
        return JsonResponse({'error': 'Cart not found'}, status=400)
    
class CheckoutTemplateView(LoginRequiredMixin,TemplateView):
    template_name='customer_pages/checkout.html'