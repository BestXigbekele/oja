def calculate_cart_total(cart):
    total = 0
    totl=[]
    for amount in cart.values():
      q=float(amount['price'] * amount['quantity'])
      totl.append(q)
      p=sum(i for i in totl)
         
    return p

def get_total_quantity(request):
    # Retrieve the cart from the session
    cart = request.session.get('cart', {})
    
    # Calculate the total quantity of items in the cart
    total_quantity = sum(cart.values())
    
    return total_quantity