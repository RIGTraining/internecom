from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
# Import necessary modules and models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *


def home(request):
    return render(request, 'home.html')


def login_page(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
        if not User.objects.filter(username=username).exists():
            
            messages.error(request, 'Invalid Username')
            return redirect('/login/')
        
        
        user = authenticate(username=username, password=password)
        
        if user is None:
           
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            
            login(request, user)
            return redirect('/')
    
    
    return render(request, 'login.html')


def register_page(request):
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
        user = User.objects.filter(username=username)
        
        if user.exists():
            
            messages.info(request, "Username already taken!")
            return redirect('/register/')
        
        
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        
        
        user.set_password(password)
        user.save()
        
       
        messages.info(request, "Account created Successfully!")
        return redirect('/register/')
    
    
    return render(request, 'register.html')

@login_required(login_url='login_page')
def shopview(request):
    itm = Items.objects.all()
    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        context = {'itm':itm, 'cart':cart}
        return render(request, 'shop.html', context)
    else:
        cart = None
        context = {'itm':itm, 'cart':cart}
        return render(request, 'shop.html', context)
    
    
    


@login_required(login_url='login_page')
def addtowhitlist(request):
    itemid = request.GET.get('iid')
    # Wishlist
    item_obj = Items.objects.get(id=itemid)
    w = Wishlist.objects.create(usr=request.user, item=item_obj)
    return JsonResponse({'status':'success'})

def whitelistview(request):
    
    context = {}
    return render(request, 'shop.html', context)

#Add to Cart Function
def addtocart(request):
    product_id = request.GET.get('iid')
    quantity = request.GET.get('quantity')
    product_obj = Items.objects.get(id=product_id)
    cart_id = request.session.get("cart_id", None)
    
    if cart_id:
        cart_obj = Cart.objects.get(id=cart_id)
        this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
        # Product already exists in cart
        if this_product_in_cart.exists():
            pass
        # New item added in cart
        else:
            subtotal = int(quantity) * product_obj.sell_price
            item_filter = Items.objects.filter(id=product_id)
            cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj,rate=product_obj.sell_price, quantity=int(quantity), subtotal=subtotal)
            cart_obj.total += subtotal
            cart_obj.save()
    else:
        cart_obj = Cart.objects.create(total=0, usr=request.user)
        request.session['cart_id'] = cart_obj.id
    
    return JsonResponse({'status':'success'})

