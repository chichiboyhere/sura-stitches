from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import *
from django.http import JsonResponse
import json
import datetime
from . utils import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
# from django.contrib.auth.decorators import login_required


# https://studygyaan.com/django/how-to-add-gmail-log-in-in-django


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {"cartItems": cartItems}
    return render(request, "store/store.html", context)

def products(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    context = {"products": products, "cartItems": cartItems}
    return render(request, "store/products.html", context)

def product(request, product_id):
	data= cartData(request)
	cartItems= data['cartItems']
	product = Product.objects.get(pk=product_id)
	context = {"product": product, "cartItems": cartItems}
	return render(request, "store/product-detail.html", context)
  

def cart(request):
	data = cartData(request)
	cartItems=data['cartItems']       # total number of items order
	order= data['order']              # a customer's order
	items = data['items']             # orderItems(products ordered, their quantity, size)
	context={"items": items, "order": order, "cartItems": cartItems, 'shipping':False}
	return render(request, 'store/cart.html', context )


def checkout(request):
	data = cartData(request)
	cartItems=data['cartItems'] 
	order= data['order']
	items = data['items']
	context = {"items": items, "order": order, "cartItems": cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	#
	# orderItem.size = data['size']
    
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer= customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    

	if action == 'add':
		orderItem.quantity = orderItem.quantity + 1
	elif action == 'remove':
		orderItem.quantity = orderItem.quantity - 1
    
	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()
	return JsonResponse('Item was added', safe=False)


def intialAddToCart(request):
    data = json.loads(request.body)
    productId = data['productId']
    size = data['size']
    product = Product.objects.get(id=productId)
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer= customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    orderItem.quantity += 1
    orderItem.size = size
    orderItem.save()
    return JsonResponse('Item added to cart', safe=False)
      

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer= customer, complete=False)
		
	else:
		customer, order = guestOrder(request, data)
		

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()
	if order.shipping == True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address= data['shipping']['address'],
			city= data['shipping']['city'],
			state= data['shipping']['state'],
			zipcode= data['shipping']['zipcode']
			)
	return JsonResponse('Payment complete', safe=False)

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("store"))
        else:
            return render(request, "store/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "store/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("store"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "store/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            regCustomer, created = Customer.objects.get_or_create(user= user, name=request.POST["username"],email = request.POST["email"] )
            regCustomer.save()
        except IntegrityError:
            return render(request, "store/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("store"))
    else:
        return render(request, "store/register.html")


def ourStory(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {"cartItems": cartItems}
    return render(request, "store/ourStory.html", context)

def contact(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {"cartItems": cartItems}
    return render(request, "store/contact.html", context)

def contactMessage(request):
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        name = customer.name
        email = customer.email
        subject = data['form']['subject']
        message = data['form']['message']
    else:
        name = data['form']['name']
        email = data['form']['email']
        subject = data['form']['subject']
        message = data['form']['message']
    ContactMessage.objects.create(
          name=name,
          email=email,
          subject=subject,
          message=message
    )
    return JsonResponse('message received', safe=False)
	
    
