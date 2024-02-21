from .models import Category, Address

def default(request):
    categories = Category.objects.all()
    address = None
    name=request.user.username

    if request.user.is_authenticated:
        try:
            # Retrieve the default address for the user
            address = Address.objects.get(user=request.user, status=True)
        except Address.DoesNotExist:
            # Handle the case where the default address doesn't exist
            pass
        except Address.MultipleObjectsReturned:
            # Handle the case where multiple default addresses are found
            # You may want to log this occurrence for further investigation
            pass
    
    return {
        'categories': categories,
        'address': address,
        'name':name
    }
