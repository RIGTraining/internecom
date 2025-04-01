from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, View, CreateView, DetailView,FormView
from django.urls import reverse_lazy
# Create your views here.
# Import necessary modules and models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator

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
    white_list = Wishlist.objects.filter(usr = request.user)
    context = {'white_list':white_list}
    return render(request, 'wishlist.html', context)

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
        subtotal = int(quantity) * product_obj.sell_price
        item_filter = Items.objects.filter(id=product_id)
        cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj,rate=product_obj.sell_price, quantity=int(quantity), subtotal=subtotal)
        cart_obj.total += subtotal
        cart_obj.save()
        
    
    return JsonResponse({'status':'success'})


def cartview(request):
    cart_id = request.session.get("cart_id", None)
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        context = {'cart':cart}
        return render(request, 'cartview.html', context)
    else:
        context={}
        return render(request, 'cartview.html', context)
    
    
    
    

def clearcart(request):
    cart_id = request.session.get("cart_id", None)
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        cart.cartproduct_set.all().delete()
        cart.total =0
        cart.save()
        return JsonResponse({'status':'success'})


def processtocheck(request):
    # Coupon, country, state, address
    cart_id = request.session.get("cart_id", None)
    cart = Cart.objects.get(id=cart_id)
    Coupon = request.GET.get('Coupon')
    country = request.GET.get('country')
    state = request.GET.get('state')
    address = request.GET.get('address')
    # print(Coupon, country, state, address)
    ItemOrder.objects.create(cart=cart, discount_code=Coupon, country=country, state=state, address=address)
    request.session['cart_id'] = None
    # del request.session['cart_id']
    return JsonResponse({'status':'success'})



# ===================================================User Log In ===============================
from django import forms
from .models import *


class ULoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class UserRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        # if request.user.is_authenticated & request.user.is_superuser:
        if request.user.is_staff:
            pass
        else:
            return redirect('UserLoginView')
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(FormView):
    template_name = 'login.html'
    form_class = ULoginForm
    success_url = reverse_lazy('shopview')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data['password']
        usr = authenticate(username=username, password=password)

        if usr is not None:
            login(self.request, usr)

        else:
            return render(self.request, self.template_name, {'form': self.form_class, 'error': 'Invalid user login!'})
        return super().form_valid(form)

class UserLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('UserLoginView')


class AdminReportList(UserRequiredMixin,View):
    def get(self, request):
        datas = ItemOrder.objects.all()
        paginator = Paginator(datas, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context={'datas':datas, 'page_obj':page_obj}
        return render(request, 'AdminReportList.html', context)

class OrderDetailsView(UserRequiredMixin,View):
    def get(self, request, pk):
        rep = ItemOrder.objects.get(id=pk)
        cart_id = rep.cart
        # print(cart_id)
        cart = Cart.objects.get(id=cart_id.id)
        context = {'cart':cart}
        return render(request, 'OrderDetailsView.html', context)

class AdminDash(UserRequiredMixin,View):
    def get(self, request):
        context = {}
        return render(request, 'AdminDash.html', context)
    
class AdminProductManagement(View):
    def get(self, request):
        cat = Category.objects.all()
        # sub = subCategory.objects.all()
        itm = Items.objects.all()
        context = {'cat':cat, 'itm':itm}
        return render(request, 'AdminProductManagement.html', context)