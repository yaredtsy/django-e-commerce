from django.shortcuts import get_object_or_404, render
from .models import Product,Category
from cart.models import CartItem
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

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
    paginator = Paginator(products,2)

    page = request.GET.get('page')
    paged_product = paginator.get_page(page)

    context = {
        'products': paged_product,
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

def search(request):
    product_count = 0
    products = None

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()

    context = {
        'products':products,
        'product_count':product_count,
    }
    return render(request,'store/store.html',context)