# context_processors.py
from .utility import calculate_cart_total,get_total_quantity
from .models import products ,CartItem,SubCategory # Assuming you have a Product model



def cart_total(request):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(cart__user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_item)
        total_items = cart_item.count()
    else:
        cart_item = request.session.get('cart', {})
        total_price = 0
        total_items = 0

        for item in cart_item.values():
            total_price += float(item['price']) * item['quantity']  # Calculate total price
            total_items += item['quantity']  # Count total items
  
    return {'total_price': total_price,'total_items': total_items,'cart_item':cart_item}


def cart_quantity(request):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(cart__user=request.user)
        total_quantity = cart_item.count()
        print(total_quantity)
    else:
        cart = request.session.get('cart', {})
        total_quantity =len(cart)
        
    return {}


def search(request):
     
    search_query = request.GET.get('search', '')

    # Get products based on the search query
    products_item= products.objects.filter(name__icontains=search_query) if search_query else products.objects.none()
    
    # Get all categories (for filter dropdown)
    categories = SubCategory.objects.all()

    return {
        'products': products,
        'categories': categories,
        'search_query': search_query,
    }