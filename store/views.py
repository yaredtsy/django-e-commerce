from django.shortcuts import get_object_or_404, render
from .models import Product,Category
from cart.models import CartItem

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def store(request,category_slug=None):
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

def product_detail(request,category_slug,product_slug):
    in_cart=False
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request,'store/product_detail.html',context)