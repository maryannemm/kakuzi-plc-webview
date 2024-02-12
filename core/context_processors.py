# core/context_processors.py

from .models import Category, Address

def default(request):
    categories = Category.objects.all()
    address = None

    if request.user.is_authenticated:
        try:
            address = Address.objects.get(user=request.user)
        except Address.DoesNotExist:
            # Handle the case where the address doesn't exist
            pass
    
    return {
        'categories': categories,
        'address': address,
    }
