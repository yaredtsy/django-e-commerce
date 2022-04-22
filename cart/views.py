from ast import Try
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist 
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id= _cart_id(request))
       
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id= _cart_id(request)
        )
        cart.save()

    is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()


    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product,cart=cart)

        ex_var_list = []
        id = []

        for item in cart_item:
            existing_variation = item.variation.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)


        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product,id=item_id)
            item.qunatity +=1
            item.save()
        else:
            item = CartItem.objects.create(product=product,qunatity=1,cart= cart)

            if len(product_variation) > 0:
                item.variation.clear()
                item.variation.add(product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            qunatity=1,
            cart= cart,
        )
        if len(product_variation) > 0:
            cart_item.variation.clear()
           
            cart_item.variation.add(product_variation)
        cart_item.save()

    return redirect('cart')

def remove_cart(request,product_id,cart_item_id):
    cart  = Cart.objects.get(cart_id= _cart_id(request))
    product = get_object_or_404(Product,id=product_id)

    try:
        cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)

        if cart_item.qunatity >1:
            cart_item.qunatity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id= _cart_id(request))

    product = get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()

    return redirect('cart')
    
def cart(request,total=0,qunatity=0,cart_items=None):
    tax = 0
    grand_total = 0
    
    try:

        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price* cart_item.qunatity)
            qunatity+=cart_item.qunatity
        tax = (15*total)/100
        grand_total = total+tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total':total,
        'qunatity':qunatity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request, 'store/cart.html',context)