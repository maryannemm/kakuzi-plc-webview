from typing import Any
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin 
from taggit.models import Tag
from django.db.models import Avg,Q
from core.forms import ProductReviewForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import JsonResponse
from django.http import  HttpResponseRedirect
from django.utils import timezone
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from .forms import CustomerAddressForm, ShippingCompanyForm, ContactUsForm, EditCustomerProfileForm, CustomerFeedbackForm
from django.urls import reverse_lazy
from .models import Category, Product, CartOrder, CartOrderItems, ProductReview, WishList, Address, ShippingCompany, ContactUs, Feedback
from userauths.models import CustomerUserRole




# Create your views here.
class HomeTemplateView(TemplateView):
    template_name = "customer_pages/index.html"
    model=Feedback
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        feedbacks=Feedback.objects.all()
        context["feedbacks"] = feedbacks
        return context
        
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
        if ProductReview.objects.filter(product=product, user=self.request.user.customeruserrole).exists():
            messages.warning(self.request, 'You already reviewed this product.', extra_tags='custom-alert-danger')
            product.user_reviewed = True
            return redirect('core:product-detail', pid=pid)
        else:
            product.user_reviewed = False

        form.instance.product = product
        form.instance.user = self.request.user.customeruserrole

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
        quantity = int(request.POST.get('quantity'))
        image = request.POST.get('image')
        db = int(request.POST.get('db'))


        if quantity <= db:

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
            # Return a JSON response with the success message and total number of items
            return JsonResponse({
                'message': 'Product added to cart successfully',
                'total_items': total_items,
                'total_price': total_price,
                'cart_items': cart_order['items'],
                'image': image ,
            })
        else:
            return JsonResponse({'error': 'Requested quantity exceeds available quantity'}, status=400)   
    
class CartListView(LoginRequiredMixin, TemplateView):
    template_name = 'customer_pages/cart.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        
        # Retrieve cart order items from the session
        cart_order_items = self.request.session.get('cart_order', {}).get('items', [])
        
        # Initialize total items and total price
        total_items = sum(item['quantity'] for item in cart_order_items)
        total_price = sum(float(item['price']) * int(item['quantity']) for item in cart_order_items)
        delivery=200
    
        
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
        context['delivery'] = delivery
        context['final_price']=total_price+delivery
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
    
        try:
            product = Product.objects.get(pid=pid)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=400)

        if quantity <= product.quantity_available:

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
        else:
            return JsonResponse({'error': 'Requested quantity exceeds available quantity'}, status=400 )
            
class CheckoutTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'customer_pages/checkout.html'
    form_class_address=CustomerAddressForm
    form_class_shipping=ShippingCompanyForm



    def post(self, request, *args, **kwargs):
        form_address = CustomerAddressForm(request.POST)
        form_shipping = ShippingCompanyForm(request.POST)

        # Check if all existing addresses have status=False
        addresses = Address.objects.filter(user=self.request.user)
        all_statuses_false = all(address.status == False for address in addresses)
        # Set status based on all_statuses_false
        status = all_statuses_false

        if form_address.is_valid() and form_shipping.is_valid():
            # Process the address form
            address_data = form_address.cleaned_data
            customer_address = Address.objects.create(
            first_name=address_data['first_name'],
            last_name=address_data['last_name'],
            address=address_data['address'],
            status=status, 
            phone=address_data['phone'],
            city=address_data['city'],
            county=address_data['county'],
            country=address_data['country'],
            user=request.user
        )
            

            # Process the shipping company form
            shipping_company_name = form_shipping.cleaned_data['company_name']
            try:
                shipping_company = ShippingCompany.objects.get(company_name=shipping_company_name)
            except ShippingCompany.DoesNotExist:
                shipping_company = form_shipping.save(commit=False)
                shipping_company.added_by = self.request.user.customeruserrole,
                shipping_company.save()

            return redirect(request.path_info)
        else:
            # If either form is invalid, return error messages
            address_errors = form_address.errors.as_json()
            shipping_errors = form_shipping.errors.as_json()
            return render(request, self.template_name, {
            'form_address': form_address,
            'form_shipping': form_shipping,
            'address_errors': address_errors,
            'shipping_errors': shipping_errors
        })

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        request = self.request
        # Check if the cart order exists in the session
        if 'cart_order' in request.session:
            cart_order = request.session['cart_order']
        else:
            context['error'] = 'Cart not found'
            return context
        # Access the request object using self.request
        
        checkout_amount = sum(float(item['price']) * item['quantity'] for item in cart_order['items'])
        order=CartOrder.objects.create(
            user=request.user.customeruserrole, 
            price=checkout_amount,

        )
        
        for item in cart_order['items']:
            cart_order_items=CartOrderItems.objects.create(
                order=order,
                invoice_number='INVOICE_NO'+str(order.id),
                item= item['title'],
                image=item['image'],
                qty=item['quantity'],
                price=item['price'],
                total= float(item['quantity'])*float(item['price'])
            )
            
        paypal_amount_usd= float(checkout_amount/150)
        paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": paypal_amount_usd,
        "item_name": "Order-item-no"+ str(order.id),
        "invoice": 'INVOICE_NO'+str(order.id),
        "currency_code":'USD',
        "notify_url": request.build_absolute_uri(reverse('core:paypal-ipn')),
        "return": request.build_absolute_uri(reverse('core:paypal_success')),
        "cancel_return": request.build_absolute_uri(reverse('core:paypal_error')),
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        
        
        checkout_amount = sum(float(item['price']) * item['quantity'] for item in cart_order['items'])
        delivery=200
        final=checkout_amount+delivery
        total_items = sum(item['quantity'] for item in cart_order['items'])
        context["checkamount"] = checkout_amount
        context['final_amount']=final
        context['delivery']=delivery
        context["total"] = total_items
        context["items"] = cart_order
        context['form']=form
        context['username']=request.user.username
        context['form_address'] = self.form_class_address
        context['form_shipping'] = self.form_class_shipping
        context['shipping_companies']= ShippingCompany.objects.all()
        context["addresses"] = Address.objects.filter(user=self.request.user, status=True)
        
        return context

class PayPalSuccessView(LoginRequiredMixin ,TemplateView):
    template_name = 'customer_pages/invoice.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Access the cart order from the session
        if 'cart_order' in self.request.session:
            cart_order = self.request.session['cart_order']
        else:
            return JsonResponse({'error': 'Cart not found'}, status=400)

        # Calculate checkout amount and total items
        checkout_amount = sum(float(item['price']) * item['quantity'] for item in cart_order['items'])
        mpesa_code = self.request.GET.get('mpesa_code')
        cart_order_items = self.request.session.get('cart_order', {}).get('items', [])

        # Update product quantity
        for item in cart_order_items:
            product_pid = item.get('pid')
            quantity = item.get('quantity')

            # Retrieve the product using the pid field
            product = get_object_or_404(Product, pid=product_pid)

            # Check if the product exists
            if product is not None:
                # Subtract the purchased quantity from the product's quantity
                product.quantity_available -= quantity
                # Save the updated product
                product.save()

        # Add necessary data to the context
        context["checkout_amount"] = checkout_amount
        context["order_items"] = cart_order_items
        context['request']=self.request
        context['mpesa_code'] = mpesa_code
        context["current_date"] = timezone.now()
        # Empty the cart session after successful checkout
        self.request.session['cart_count'] = 0
        del self.request.session['cart_order']
        

        return context    
    
class PayPalCancelView(View):
    def get(self, request, *args, **kwargs):
        # User canceled the payment
        return HttpResponseRedirect(reverse("customer_pages/payment_cancel.html"))

class PayPalErrorView(View):
    def get(self, request, *args, **kwargs):
        # Error occurred during the payment process
        return HttpResponseRedirect(reverse("customer_pages/payment_error.html"))

class PaymentSuccessView(View):
    def get(self, request, *args, **kwargs):
        # Payment was successfully completed
        return HttpResponseRedirect(reverse("customer_pages/invoice.html"))

class PaymentErrorView(View):
    def get(self, request, *args, **kwargs):
        # Error occurred during payment
        return HttpResponseRedirect(reverse("customer_pages/payment_error.html"))
    
class CustomerDashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name='customer_pages/customer_dasboard.html'
    Model= CustomerUserRole

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        customer_profile=get_object_or_404(self.Model, email=self.request.user.email)
        context["profile"] = customer_profile
        return context

class CustomerOrdersListView(LoginRequiredMixin, ListView):
    template_name='customer_pages/cusomer_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return CartOrder.objects.filter(user=self.request.user.customeruserrole).order_by('-order_date')

class CustomerOrderDetailView(LoginRequiredMixin, DetailView):
    template_name='customer_pages/customer_order_detail.html'

    def get_object(self) -> Model:
        order_id = self.kwargs.get('order_id')  # for  pass the order_id in the URL
        return CartOrder.objects.get(id=order_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('order_id')  
        context['order_items'] = CartOrderItems.objects.filter(order__id=order_id)
        return context
    
class CustomerAddressTemplateView(LoginRequiredMixin, TemplateView):
    models=Address
    template_name='customer_pages/customer_address.html' 

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["addresses"] = Address.objects.filter(user=self.request.user)
        
        return context

class CustomerEditAddressUpdateView(LoginRequiredMixin, UpdateView):
    pass

class CustomerAddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('core:customer-address', kwargs={'username': username})    
    
class CustomerDefaultAddressUpdateView(LoginRequiredMixin, UpdateView):
    model=Address
    fields = ['status']
    template_name='customer_pages/customer_Address_form.html'
    def form_valid(self, form):
        # Get the address instance being updated
        address = form.instance

        # Check if any other address has status=True
        existing_default_address = Address.objects.filter(user=self.request.user, status=True).exclude(pk=address.pk)
        if existing_default_address:
            # If another default address exists, set its status to False
            existing_default_address.status = False
            existing_default_address.save()

        # Set status=True for the current address
        address.status = True
        address.save()

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the customer address page after updating
        return reverse_lazy('core:customer-address', kwargs={'username': self.request.user.username})

class CustomerCreatetAddressUpdateView(LoginRequiredMixin, FormView):
    form_class=CustomerAddressForm
    template_name='customer_pages/customer_Address_form.html'  
    success_message='Created Address Successfully!'

    def get_success_url(self):
        # Assuming 'customer-address' requires a username argument
        username = self.request.user.username
        return reverse('core:customer-address', kwargs={'username': username})

    def form_valid(self, form):
        # Process the form data here (save to the database, etc.)
        
        customer_address=Address.objects.create(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            address=form.cleaned_data['address'],
            phone=form.cleaned_data['phone'],
            city=form.cleaned_data['city'],
            county=form.cleaned_data['county'],
            country=form.cleaned_data['country'],
            user=self.request.user

        )
        messages.success(self.request, 'Address created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle invalid form submission here
        return super().form_invalid(form)

class AddWishlistView(LoginRequiredMixin ,View):
    def post(self, request):
        if request.method == 'POST':
            product_id=request.POST.get('id')

            if product_id:
                try:
                    product=Product.objects.get(id=product_id)
                    if WishList.objects.filter(product=product, user=self.request.user.customeruserrole,).exists():
                        return JsonResponse({'success': False, 'message': 'Product already exists in wishlist.'})
                    else:
                        wishlist = WishList.objects.create(
                            product=product,
                            user=self.request.user.customeruserrole,
                        )
                        return JsonResponse({'success': True})
                except Product.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'Product does not exist.'})

            else:
                return JsonResponse({'success': False, 'message': 'Product ID parameter is missing.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method. Only POST requests are allowed.'})

class WishListListView( LoginRequiredMixin,ListView):
    model=WishList
    template_name=  'customer_pages/wishlist.html' 

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["wishlist_items"] =WishList.objects.filter(user=self.request.user) 
        return context
    
class WishlistItemDeleteView(View):
    def post(self, request, pid):
        WishList.objects.filter(product__pid=pid, user=request.user).delete()
        return HttpResponseRedirect(reverse_lazy('core:wishlist', kwargs={'username': self.request.user.username}))

class AboutUsTemplateView(TemplateView):
    template_name='customer_pages/about.html'    

class ContactUsView(FormView):
    template_name = 'customer_pages/contact.html'
    form_class = ContactUsForm

    def form_valid(self, form):
        ContactUs.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            subject=form.cleaned_data['subject'],
            message=form.cleaned_data['message']
        )
        messages.success(self.request, 'Your message was sent successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:index')

class EditCustomerProfileView(FormView):
    form_class=EditCustomerProfileForm
    template_name='customer_pages/customer_profile_edit.html'

    def form_valid(self, form):
        user=self.request.user
        profile=get_object_or_404(CustomerUserRole, email=self.request.user.email)

        profile.image=form.cleaned_data['image']
        profile.full_name=form.cleaned_data['full_name']
        profile.bio=form.cleaned_data['bio']
        profile.user=user

        profile.save()
        return super().form_valid(form)
    def get_success_url(self):
         return reverse_lazy('core:customer-dashboard' , kwargs={'username': self.request.user.username})

class CustomerFeedbackFormView(LoginRequiredMixin, FormView):
    template_name='customer_pages/feedback.html'
    form_class=CustomerFeedbackForm
    model=Feedback

    def form_valid(self, form):
        if self.request.user.verified:
            user=self.request.user
            feedback=Feedback.objects.create(
                user=user,
                message=form.cleaned_data['message']
            )
            messages.success(self.request, 'Feedback submitted successfully.')
            return super().form_valid(form)
        else :
            messages.error(self.request, 'You need to be a verified user to submit feedback.')
            return redirect('core:home')
    def get_success_url(self) -> str:
        return reverse_lazy('core:index')
       
