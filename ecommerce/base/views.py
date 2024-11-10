# store/views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.http import Http404
from .models import Product,Cart,CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout as auth_logout
from .forms import LoginForm,UserRegisterForm

def homepage(request):
    p_phone = Product.objects.all()[:4]
    p_airbud = Product.objects.all()[4:8]
    p_beauty = Product.objects.all()[8:12]
    p_puma = Product.objects.all()[12:16:3]
    p_watch = Product.objects.all()[17:20:2]
    context={
        "p_phone":p_phone,
        "p_airbud":p_airbud,
        "p_beauty": p_beauty,
        "p_puma":p_puma,
        "p_watch":p_watch
    }
    return render(request,'Home.html',context)

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            return redirect('login')  # Redirect to the login page after successful signup
    else:
        form = UserRegisterForm()  # Define form for GET requests

    return render(request, 'signup.html', {'form': form})  # Use 'form' here
    
def login_view(request):
    print("Login view accessed")  # Check if this view is hit
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Attempting to authenticate user: {username}")  # Debug info
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("User authenticated successfully")  # Debug info
                login(request, user)  # Make sure this is correct
                return redirect('homepage')
            else:
                print("Authentication failed")  # Debug info
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    auth_logout(request)  # Log out the user
    return redirect('homepage')  # Redirect to the home page or login page

def contact_view(request):
    return render(request, 'contact.html')

def about_view(request):
    return render(request, 'about.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def Product_detail(request,id):
    product = Product.objects.get(id=id)
    return render(request, 'product_detail.html', {'product': product})

    

def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:  # If the item already exists in the cart
            cart_item.quantity += 1
            cart_item.save()
        

        return redirect('cart_view')  # Redirect to cart view or wherever you want
    # Redirect to login if user is not authenticated


# views.py
@login_required
def cart_view(request):
    # Try to get the cart or create it if it doesn't exist
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get all cart items associated with this cart and calculate total price for each
    cart_items = cart.cartitem_set.all()
    for item in cart_items:
        item.total_price = item.product.price * item.quantity  # Calculate total price per item

    return render(request, 'cart.html', {'cart_items': cart_items})


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)

    # Get the CartItem associated with the product
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    
    if cart_item:
        cart_item.delete()  # Remove the item from the cart

    # Redirect to the cart page after removal
    return redirect('cart_view')  # Assuming your cart page is named 'cart_view'

def quantity(request, product_id, action):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)

    # Get the CartItem associated with the product
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    
    if cart_item:
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()  # Remove the item if quantity is 0

    # Redirect to the cart page after updating the quantity
    return redirect('cart_view')  # Assuming your cart page is named 'cart_view'
    