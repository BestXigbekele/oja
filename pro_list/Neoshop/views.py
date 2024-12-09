from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import products,Cart,SubCategory,CartItem,Order
from django.contrib.auth import authenticate,login,logout
from .forms import ProForm,CatForm,SignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
   
   men = products.objects.filter(category2__category='men')[:8]
   women = products.objects.filter(category2__category='women')[:8]
   kids = products.objects.filter(category2__category='kids')[:8]
   Accessories = products.objects.filter(category2__category='Accessories')[:8]
   hot_items = products.objects.filter(category2__category='hot items')
   on_sale = products.objects.filter(category2__category='on sale')[:3]
   best_seller = products.objects.filter(category2__category='best seller')[:3]
   Top_viewed= products.objects.filter(category2__category='top view')[:3]
   return render(request,'index.html',{'Accessories':Accessories,'men':men,'women':women,"kids":kids,"hot_items":hot_items,"on_sale":on_sale,'best_seller':best_seller,'top_viewed':Top_viewed})


def product_by_cate(request,category=None):
    if category:
        product_list = products.objects.filter(category2__category=category)
        category=SubCategory.objects.filter(category=category)
    else:
        product_list = products.objects.all()
        category="All Products"
    
    paginator = Paginator(product_list, 3)  
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request,'products.html',{'product_list': product_list,'category':category,'page_obj': page_obj})



def product_detail(request,proname):
    item=products.objects.get(name=proname)
    context={
        'item':item,}
    return render(request,'product_details.html',context) 

'''//////////////////carts////////////

/////////////////cart/////////////////
'''







def add_to_cart(request, product_id):
    product = get_object_or_404(products, id=product_id)
    cart = request.session.get('cart', {})
    
    if isinstance(cart, list):
        print("Error: Cart is a list. Converting to dictionary.") 
        cart ={}
    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {'name': product.name, 'price': str(product.price), 'quantity': 1, 'image':product.image.url}
    
    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    cart1 = request.session.get('cart', {})
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    
        for product_id, item in cart1.items():
            product = get_object_or_404(products, id=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += item['quantity']
            else:
                cart_item.quantity = item['quantity']
            cart_item.save()
        
        cart_app = CartItem.objects.all()
        
        total_price = sum(item.product.price * item.quantity for item in cart_app)
        request.session['cart'] = {}
        return render(request, 'cart2.html', { "cart_app":cart_app,'total_price':total_price})
    else:
        cart_app=[]
        total_price=0
    
        for product_id,details in cart1.items():
            item_total = float(details['price']) * details['quantity']
            total_price+=item_total
            cart_app.append({
                'product_id':product_id,
                'name':details['name'],
                'price': details['price'], 
                'quantity': details['quantity'],
                'pic':details['image'],
                'item_total':item_total
            })
           

        return render(request, 'cart.html', { "cart_app":cart_app,'total_price':total_price})


def incremental(request,product_id):
    cart1 = request.session.get('cart', {})
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(product_id=product_id)
        cart_item.quantity += 1
        cart_item.save()
        cart_app = CartItem.objects.all()
        total_price = sum(item.product.price * item.quantity for item in cart_app)
    else:
        for product_id,details in cart1.items():
            item_total =  details['quantity']
            item_total+=1
        print(f'geeggeegge{item_total}')

    return JsonResponse({
        'item_price':cart_item.product.price * cart_item.quantity,
        'quantity': cart_item.quantity,
        'total_price':total_price
    })

def decrement(request,product_id):
    cart_item=CartItem.objects.get(product_id=product_id)
    if cart_item.quantity > 1:
        cart_item.quantity-=1
        cart_item.save()
    cart_app = CartItem.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_app)
    
    return JsonResponse({
        'quantity':cart_item.quantity,
        'item_price':cart_item.quantity*cart_item.product.price,
        'total_price':total_price
    })



@login_required(login_url='register')
def checkout(request):
    cart=Cart.objects.get(user=request.user)
    items=CartItem.objects.all()
    total_amount = sum(item.product.price * item.quantity for item in items)
    if request.method=="POST":
        shopping_add=request.POST.get('Shopping_Address')
        total_amount = sum(item.product.price * item.quantity for item in items)
        
        order=Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            shipping_address=shopping_add
            
        )

        cart.items.all().delete()
        return redirect('checkout_confirmation',order_id=order.id)
    print(f'total_amount:{total_amount}' )
    return render(request, 'checkout.html', {'items':items,"total_amount":total_amount})

def confirmation(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'success.html', {"order":order})



def remove_from_cart(request,product_id):
    cart = request.session.get('cart', {})
    if request.user.is_authenticated:
        cart_app = CartItem.objects.get(product_id=product_id)
        cart_app.delete()
        return redirect('cart')

    else:
        print(f'se year {cart}')
        if str(product_id) in cart:
            del cart[str(product_id)]
            request.session['cart'] = cart 
        return redirect('cart')

   

    
def login_user(request):
    context={}
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return redirect('register')
    else:
        return render(request,'login.html',context)




def registeruser(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'u have side in') 
            return redirect('home')
        else:
            messages.success(request,'u have no not in') 
            
    else:
        form = SignUpForm()
        
    return render(request, 'register.html', {'form': form})
 
    

    









 
def logout_user(request):
    logout(request)
    return redirect('home')




def admin_site(request):
    if request.method == "POST":
        form=ProForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success('sucess')
            return redirect('home')
    else:
        form=ProForm()
        
    return render(request,'admin-site.html',{'form':form})
    




