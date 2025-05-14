from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from .models import Buyer, Seller
from django.http import HttpResponse
from .models import ProductSale
from django.utils.timezone import now
from .models import OrganicProduct, OrganicManure,Order
from .forms import OrganicProductForm, OrganicManureForm
from .sms_service import send_sms




def index(request):
    return render(request, 'landing/index.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            city = form.cleaned_data['city']
            role = form.cleaned_data['role']

            if role == 'buyer':
                Buyer.objects.create(username=username, password=password, city=city)
            else:
                Seller.objects.create(username=username, password=password, city=city)

            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = SignupForm()

    return render(request, 'landing/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']

            if role == 'buyer':
                try:
                    user = Buyer.objects.get(username=username, password=password)
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    request.session['role'] = 'buyer'
                    return redirect('profile')  # Redirect to profile after successful login
                except Buyer.DoesNotExist:
                    form.add_error(None, 'Invalid credentials')
            else:
                try:
                    user = Seller.objects.get(username=username, password=password)
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    request.session['role'] = 'seller'
                    return redirect('profile')  # Redirect to profile after successful login
                except Seller.DoesNotExist:
                    form.add_error(None, 'Invalid credentials')
    else:
        form = LoginForm()

    return render(request, 'landing/login.html', {'form': form})

def profile_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    user_id = request.session['user_id']
    role = request.session['role']
    
    if role == 'buyer':
        user = Buyer.objects.get(id=user_id)
        context = {
            'username': user.username,
            'city': user.city,
            'role': role.capitalize()
        }
    else:  # seller
        user = Seller.objects.get(id=user_id)
        
        # Sample sales data (in a real application, this would come from a database)
        sales_data = {
            'total_sales': 150000,  # in rupees
            'total_products_sold': 750,  # in kg
            'monthly_sales': [
                {'month': 'Jan', 'amount': 12000},
                {'month': 'Feb', 'amount': 15000},
                {'month': 'Mar', 'amount': 18000},
                {'month': 'Apr', 'amount': 20000},
                {'month': 'May', 'amount': 22000},
                {'month': 'Jun', 'amount': 25000},
            ],
            'top_products': [
                {'name': 'Compost', 'quantity': 300, 'revenue': 60000},
                {'name': 'Vermicompost', 'quantity': 250, 'revenue': 62500},
                {'name': 'Bio-fertilizer', 'quantity': 200, 'revenue': 60000},
            ],
            'recent_orders': [
                {'product': 'Compost', 'quantity': 50, 'amount': 10000, 'date': '2024-03-15'},
                {'product': 'Vermicompost', 'quantity': 30, 'amount': 7500, 'date': '2024-03-14'},
                {'product': 'Bio-fertilizer', 'quantity': 25, 'amount': 7500, 'date': '2024-03-13'},
            ]
        }
        
        context = {
            'username': user.username,
            'city': user.city,
            'role': role.capitalize(),
            'sales_data': sales_data
        }
    
    return render(request, 'landing/profile.html', context)

def organic_products_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    context = {
        'products': [
            {
                'name': 'Compost',
                'price': '₹200/kg',
                'description': 'High-quality organic compost made from kitchen waste',
                'nitrogen': '1.5%',
                'phosphorus': '0.8%',
                'potassium': '1.2%',
                'organic_carbon': '25-30%',
                'c_n_ratio': '20-25:1',
                'ph': '6.5-7.5',
                'moisture': '30-35%',
                'suitable_crops': 'Vegetables (Tomato, Brinjal, Chilli), Fruits (Mango, Banana, Citrus), Flowers (Rose, Marigold), Herbs (Basil, Mint)',
                'application_rate': '5-10 tons per acre',
                'benefits': 'Improves soil structure, enhances water retention, promotes microbial activity, increases organic matter content',
                'storage': 'Store in dry, shaded area',
                'shelf_life': '6-12 months'
            },
            {
                'name': 'Vermicompost',
                'price': '₹250/kg',
                'description': 'Nutrient-rich vermicompost produced using earthworms',
                'nitrogen': '2.0%',
                'phosphorus': '1.2%',
                'potassium': '1.5%',
                'organic_carbon': '20-25%',
                'c_n_ratio': '15-20:1',
                'ph': '6.8-7.2',
                'moisture': '25-30%',
                'suitable_crops': 'Leafy vegetables (Spinach, Lettuce), Root crops (Carrot, Potato), Fruit trees (Apple, Guava), Ornamental plants',
                'application_rate': '3-5 tons per acre',
                'benefits': 'High nutrient content, improves soil fertility, enhances plant growth, contains beneficial microorganisms',
                'storage': 'Store in cool, dry place',
                'shelf_life': '8-12 months'
            },
            {
                'name': 'Bio-fertilizer',
                'price': '₹300/kg',
                'description': 'Organic bio-fertilizer for enhanced plant growth',
                'nitrogen': '2.5%',
                'phosphorus': '1.5%',
                'potassium': '2.0%',
                'organic_carbon': '15-20%',
                'c_n_ratio': '10-15:1',
                'ph': '7.0-7.5',
                'moisture': '20-25%',
                'suitable_crops': 'All crops, especially nitrogen-fixing plants (Legumes, Pulses), Cereals (Rice, Wheat), Oilseeds (Groundnut, Soybean)',
                'application_rate': '2-4 tons per acre',
                'benefits': 'Promotes nitrogen fixation, improves soil health, sustainable alternative to chemical fertilizers, enhances root development',
                'storage': 'Store in cool, dark place',
                'shelf_life': '12-18 months'
            },
        ]
    }
    return render(request, 'landing/organic_products.html', context)

def organic_manures_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    context = {
        'manures': [
            {
                'name': 'Cow Dung Manure',
                'price': '₹150/kg',
                'description': 'Pure cow dung manure, rich in nutrients',
                'nitrogen': '0.5%',
                'phosphorus': '0.2%',
                'potassium': '0.5%',
                'organic_carbon': '30-35%',
                'c_n_ratio': '25-30:1',
                'ph': '6.5-7.0',
                'moisture': '35-40%',
                'suitable_crops': 'Cereals (Rice, Wheat), Pulses (Chickpea, Pigeon pea), Oilseeds (Mustard, Sunflower), Vegetables',
                'application_rate': '10-15 tons per acre',
                'benefits': 'Improves soil fertility, enhances water retention, promotes microbial activity, adds organic matter',
                'storage': 'Store in covered area',
                'shelf_life': '4-6 months'
            },
            {
                'name': 'Poultry Manure',
                'price': '₹180/kg',
                'description': 'Organic poultry manure for better soil fertility',
                'nitrogen': '3.0%',
                'phosphorus': '2.5%',
                'potassium': '1.5%',
                'organic_carbon': '25-30%',
                'c_n_ratio': '15-20:1',
                'ph': '6.8-7.2',
                'moisture': '30-35%',
                'suitable_crops': 'Vegetables (Tomato, Brinjal), Flowers (Rose, Chrysanthemum), Fruit trees (Mango, Guava), Leafy greens',
                'application_rate': '5-8 tons per acre',
                'benefits': 'High nutrient content, fast-acting, improves soil structure, rich in micronutrients',
                'storage': 'Store in dry, covered area',
                'shelf_life': '3-4 months'
            },
            {
                'name': 'Green Manure',
                'price': '₹220/kg',
                'description': 'Natural green manure for sustainable farming',
                'nitrogen': '2.0%',
                'phosphorus': '0.5%',
                'potassium': '1.0%',
                'organic_carbon': '35-40%',
                'c_n_ratio': '20-25:1',
                'ph': '6.5-7.0',
                'moisture': '25-30%',
                'suitable_crops': 'Legumes (Sunnhemp, Dhaincha), Cover crops, Mixed cropping systems, Rice fields',
                'application_rate': '8-12 tons per acre',
                'benefits': 'Improves soil structure, prevents erosion, adds organic matter, fixes atmospheric nitrogen',
                'storage': 'Store in dry, ventilated area',
                'shelf_life': '6-8 months'
            },
        ]
    }
    return render(request, 'landing/organic_manures.html', context)

 
def buynow_view(request, product_type, product_name):
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login if the user is not logged in

    product = None
    if product_type == 'manure':
        product = OrganicManure.objects.filter(name=product_name).first()
    elif product_type == 'product':
        product = OrganicProduct.objects.filter(name=product_name).first()

    if not product:
        return redirect('index')  # Redirect to homepage if the product is not found

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        payment = request.POST.get('payment')

        # Deduct stock and save the order
        if quantity > product.stock:
            return render(request, 'landing/buynow.html', {
                'product_name': product.name,
                'product_type': product_type,
                'price': product.price,
                'stock': product.stock,
                'description': product.description,
                'username': request.session.get('username', 'User'),
                'error': 'Insufficient stock available.'
            })

        product.stock -= quantity
        product.save()

        # Save the order in the database
        order = Order.objects.create(
            product_name=product.name,
            product_type=product_type,
            quantity=quantity,
            price=product.price * quantity,
            phone=phone,
            address=address,
            city=city,
            state=state,
            payment_method=payment
        )

        # Send SMS to the user
        sms_message = f"OneEarthFarm - Thank you for your purchase! Your order for {quantity} unit(s) of {product.name} has been placed successfully."
        send_sms(phone, sms_message)

        # Redirect to a success page
        return render(request, 'landing/success.html', {
            'product_name': product.name,
            'quantity': quantity,
            'phone': phone,
            'address': address,
            'city': city,
            'state': state,
            'payment': payment
        })

    return render(request, 'landing/buynow.html', {
        'product_name': product.name,
        'product_type': product_type,
        'price': product.price,
        'stock': product.stock,
        'description': product.description,
        'username': request.session.get('username', 'User')
    })


sales_database = {
    "total_sales": 0,
    "total_products_sold": 0,
    "recent_sales": []
}

 

def sell_product_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not authenticated

    if request.method == 'POST':
        # Fetch data from the submitted form
        product_type = request.POST.get('product_type')
        quantity = request.POST.get('quantity')

        # Validate input
        if not product_type or not quantity.isdigit():
            return render(request, 'sell_product.html', {
                'error': 'Please provide valid product details.'
            })

        quantity = int(quantity)
        price_per_kg = 10  # Example fixed price per kg
        total_earnings = quantity * price_per_kg

        # Save the sale to the database
        ProductSale.objects.create(
            seller=request.user,
            product_type=product_type,
            quantity=quantity,
            price_per_kg=price_per_kg,
            total_earnings=total_earnings
        )

        # Redirect to a success page or render a success message
        return render(request, 'landing/sell.html', {
            'username': request.user.username,
            'product_type': product_type,
            'quantity': quantity,
            'price_per_kg': price_per_kg,
            'total_earnings': total_earnings,
        })

    # Render the sell_product.html template for GET requests
    return render(request, 'sell_product.html')

def sell(request):
    return render(request, 'landing/sell.html')

 

def organic_products_view(request):
    products = OrganicProduct.objects.all()  # Fetch all organic products
    return render(request, 'landing/organic_products.html', {'products': products})

def organic_manures_view(request):
    manures = OrganicManure.objects.all()  # Fetch all organic manures
    return render(request, 'landing/organic_manures.html', {'manures': manures})



