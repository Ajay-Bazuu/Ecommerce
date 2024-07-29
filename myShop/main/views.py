from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .form import ProfileUpdateForm, ReviewForm
from django.contrib.auth.decorators import login_required



from django.contrib.auth.decorators import login_required
from cart.cart import Cart
# Create your views here.
def index(request):
    product=Product.objects.all()
    cate=Category.objects.all()

    cateid=request.GET.get('category')
    if cateid:
        product=Product.objects.filter(subcategory=cateid)
    else:
        product=Product.objects.all()
    
# Pagination
    page=Paginator(product,4)
    page_number=request.GET.get('page')
    data=page.get_page(page_number)
    total_page=data.paginator.num_pages


    context={
        'product':product,
        'cate':cate,
        'data':data,
        'total_page':total_page,
        'num':[i+1 for i in range(total_page)]
    }
    return render(request,'main/index.html',context)

# def cart(request):
#     return render(request,'main/cart.html')

def checkout(request):

    if request.method=="POST":
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        cart=request.session.get('cart')
        uid=request.session.get('_auth_user_id')
        user=User.objects.get(pk=uid)
        print(cart)

        for i in cart:
            x=cart[i]['quantity']
            y=cart[i]['price']
            total=x*float(y)

            order=Order(
                product=cart[i]['name'],
                quantity=cart[i]['quantity'],
                price=cart[i]['price'],
                image=cart[i]['image'],
                phone=phone,
                address=address,
                user=user,
                total=total,
            )
            order.save()
        request.session['cart']={}
        return redirect('index')
    
@login_required(login_url='log_in')
def your_order(request):
    uid=request.session.get('_auth_user_id')
    user=User.objects.get(pk=uid)
    
    order=Order.objects.filter(user=user)
    return render(request,'main/your_order.html',{'order':order}) 

def contact(request):
    return render(request,'main/contact-us.html')
def log_in(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        if not User.objects.filter(username=username).exists():
            messages.info(request,"User name Does Not Exits ")
            return redirect ('log_in')
        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request," Password Mismatch ")
            return redirect('log_in')
    return render(request,'auth/login.html')


def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST["password"]
        confirm_password=request.POST['confirm_password']
        if password==confirm_password:
            User.objects.create_user(username=username,email=email,password=password)
            messages.success(request,"Registered Successfully ")
        else:
         messages.error(request,"Confirm Password and Password Mismatch ")
         return redirect("log_in")

    return render(request,'auth/login.html')


def product_detail(request,id):
    product=get_object_or_404(Product,id=id)
    
    cmt_all=request.GET.get('cmt_all')
    if cmt_all:
        reviews=product.reviews.all()
    else:
        reviews=product.reviews.all().order_by('-id')[:3]

    products=Product.objects.filter(category=product.category).exclude(id=id)
    form=ReviewForm()

    if request.method=="POST":
        form=ReviewForm(request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.product=product
            review.user=request.user
            review.save()

            return redirect('product_detail',id=id)

    context={
        'product':product,
        'products':products,
        'form':form,
        'reviews':reviews,
        'range':range(1,6)
    }

    return render(request,'main/product-details.html',context)


def shop(request):
    return render(request,'main/shop.html')
def blog_single(request):
    return render(request,'main/blog-single.html')
def blog(request):
    return render(request,'main/blog.html')

def log_out(request):
    logout(request)
    return render(request,'auth/login.html')

@login_required(login_url=log_in)
def customer_detail(request):
    profile,created=Profile.objects.get_or_create(user=request.user)
    profile_form=ProfileUpdateForm(instance=profile)

    if request.method=="POST":
        profile_form=ProfileUpdateForm(request.POST,request.FILES,instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')

    context={
        'profile_form':profile_form,
        'user':request.user,
        'profile':request.user.profile,
    }
    return render(request,'main/cutomer_details.html',context)


# Cart
# 
# 
# 

@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_detail(request):
    return render(request, 'main/cart.html')


# Khalti
import requests
import json
import uuid # generate unique transaction id
from django.http import JsonResponse

@login_required
def initkhalti(request,id):
    data=Order.objects.get(id=id)
    
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    return_url = 'http://127.0.0.1:8080/verify/'
    amount = data.total
   
    transaction_id = str(uuid.uuid4())  # Generate a unique transaction ID
    purchase_order_name = data.product
    username =data.user.username
    email = data.user.email
    phone = data.phone
    quantity=data.quantity
    owned_by=data.user.username
    # vehicle_id = request.POST.get('vehicle_id')
    # owned_by = request.POST.get('owned_by')

        # Generate a unique purchase_order_id

    purchase_order_id = data.id

    payload = json.dumps({
            "return_url": return_url,
            "website_url": return_url,
            "amount": amount,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": purchase_order_name,
            "transaction_id": transaction_id,
            "customer_info": {
                "name": username,
                "email": email,
                "phone": phone,
            },
            "product_details": [
                {
                    "identity": data.id,
                    "name": purchase_order_name,
                    "unit_price": amount,
                    "total_price": amount,
                    "quantity": quantity
                }
            ],
            "merchant_username": owned_by,
        })

    headers = {
            'Authorization': 'Key a3e802f7f23949f6847fdb4182543535',
            'Content-Type': 'application/json',
        }

    response = requests.post(url, headers=headers, data=payload)
    new_res = response.json()

    print("Khalti API Response:", new_res)  # Debugging statement

    if response.status_code == 200 and 'payment_url' in new_res:
            return redirect(new_res['payment_url'])
    else:
            return JsonResponse({'error': 'Failed to initiate payment', 'details': new_res}, status=400)

    # return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def verifyKhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    if request.method == 'GET':
        headers = {
            'Authorization': 'key a3e802f7f23949f6847fdb4182543535',
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
        transaction_id = request.GET.get('transaction_id')
        purchase_order_id = request.GET.get('purchase_order_id')
        data = json.dumps({
            'pidx':pidx
        })
        res = requests.request('POST',url,headers=headers,data=data)
        print(res)
        print(res.text)

        new_res = json.loads(res.text)
        print(new_res)
        

        if new_res['status'] == 'Completed':
            order = get_object_or_404(Order, id=purchase_order_id)

            order.isPay = True
            # vehicle.rented_by = request.user  # Assuming the user is logged in
            order.save()

            Transaction.objects.create(
                order=order,
                transaction_id=transaction_id,
                amount=new_res['total_amount'],  # Assuming amount is returned in the response
                user=request.user
            )

            # send_mail(
            #     'Vehicle Rented',
            #     f'Your vehicle {vehicle.vehicle_model} has been rented by {request.user.username}.',
            #     'sujanthadarai710@gmail.com',
            #     [vehicle.uploaded_by.email],
            #     fail_silently=False,
            # )
            return redirect('your_order')
        else:
            print("Payment verification failed. Khalti response:", json.dumps(new_res, indent=4))
            return JsonResponse({'error': 'Payment verification failed'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)