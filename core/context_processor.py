
from .models import Category, Vendor, Address


def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    address = Address.objects.get(user=request.user)
    return {
        'categories': categories,
        'vendors': vendors,
        'address': address
    }
