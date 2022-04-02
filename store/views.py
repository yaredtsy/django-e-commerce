from django.shortcuts import get_object_or_404, render
from .models import Product,Category
# Create your views here.

def store(request,category_slug):
    categoryies = None
    products  = None

    if category_slug != None:
        categoryies = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categoryies,is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True)
        
    product_count = products.count()
    context = {
        'products': products,
        'product_count':product_count,
    }
    return render(request,'store/store.html',context)