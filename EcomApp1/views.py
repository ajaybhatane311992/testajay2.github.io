from django.shortcuts import render,redirect,HttpResponseRedirect
from .forms import ProductModelForm,CustomerForm
from .models import ProductModel,CustomerModel,OrderModel,CategoryModel
from django.contrib.auth import logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password,check_password

#custom decorator for login
from .middlewares.auth import auth_middleware

from django.core.paginator import Paginator
from django.http import HttpResponse

#code for send html page on mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# code for invoice pdf
from django.template.loader import get_template
from xhtml2pdf import pisa

# otp
import random

# Create your views here.
def addView(request):
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    obj=ProductModel.objects.all()
    template_name='EcomApp1/add.html'
    context={'form':form,'obj':obj}
    return render(request,template_name,context)

def homeView(request):
    template_name='EcomApp1/home.html'
    context={}
    return render(request,template_name,context)

def storeView(request):
    #Code For AddToCart
    if request.method == "POST":
        product=request.POST.get('product')
        remove=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity= cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart={}
            cart[product] = 1
        #   for check line if cart value in line no 104
        request.session['cart'] = cart
        return redirect('store')

    # code for cart error in pipe for men.html
    cart=request.session.get('cart')
    if not cart:
        request.session.cart={}

    products=None
    categories=CategoryModel.objects.all()

    #Code for price Filter
    CategoryId=request.GET.get('category')
    if CategoryId:
        products=ProductModel.get_products_by_categoryId(CategoryId)
    else:
        products=ProductModel.objects.all()

    productbyPrice=request.GET.get('productPrice')
    if productbyPrice == 'below500':
        products=ProductModel.objects.filter(Price__lte=500)
    elif productbyPrice == 'above501':
        products = ProductModel.objects.filter(Price__gte=500)

    brandbyname = request.GET.get('brandname')
    if brandbyname == 'Levis':
        products = ProductModel.objects.filter(Name=brandbyname)
    elif brandbyname == 'Roadstar':
        products = ProductModel.objects.filter(Name=brandbyname)


    template_name='EcomApp1/store.html'
    context={'products':products,'categories':categories}
    # return HttpResponse('Done')       # check error
    return render(request,template_name,context)

def signUpView(request):    #username= ajay ,pass=@jAy12345
    form=CustomerForm()
    if request.method == 'POST':
        form=CustomerForm(request.POST)


        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = int(form.cleaned_data['phone'])
            password = form.cleaned_data['password']
            confirm_password=form.cleaned_data['confirm_password']

            if password == confirm_password:
                if CustomerModel.objects.filter(email=email).exists():
                    messages.error(request,'Email is Already Exist')

                    return redirect('signup')

                # code for otp
                SSOTP = request.session.get('SOTP')
                print('SOTP',SSOTP)
                cotp=request.POST.get('OTP')
                if not SSOTP == cotp :
                    messages.error(request,'OTP Does not match')
                    return redirect('signup')
                # end opt

                obj=CustomerModel(first_name=first_name,last_name=last_name,email=email,phone=phone,password=password)
                obj.password=make_password(obj.password)  #Password Hashing
                obj.save()
                del request.session['SOTP']
                DSOTP=request.session.get('SOTP')
                print('DSOTP',DSOTP)

                return redirect('login')
            else:
                messages.error(request, 'Password Does not match')
    template_name='EcomApp1/signup.html'
    context={'form':form}
    return render(request,template_name,context)

def loginView(request):
    return_url=None
    if request.method == 'POST':
        em=request.POST.get('email')
        password=request.POST.get('pw')
        user=CustomerModel.objects.filter(email=em)
        if user:
            for u in user:
                if check_password(password,u.password):  # return True if match #password hashing check login time (ajmal123456, pbkdf2_sha256$260000$sDaj9dGxLmsuEGsBwLYjcT$fPPl8DKZ+8snv7YVc8Wx7Cc0lryNICNx0UGJfm5wnlQ=
                    # code for Session
                    request.session['cname']=u.first_name
                    request.session['cid']=u.id
                    ######Code For Send Mail----
                    # send_mail(
                    #     'Signed-in ',  # Subject
                    #     'Hello .' + u.first_name + ',I am Ajay from AllShopping.com-Team and you are signed-in to your AllShopping account through your ,' + u.email, # msg
                    #     settings.EMAIL_HOST_USER,  # From
                    #     [u.email],  # To
                    #     fail_silently=False,
                    # )
                    ## End Send Mail

                    ##middleware Code
                    # if loginView.return_url:
                    #     return HttpResponseRedirect(loginView.return_url)
                    # else:
                    loginView.return_url=None
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid Password ! ')
                    return redirect('login')
        else:
            messages.error(request, 'Invalid Email ! ')
            return redirect('login')

    loginView.return_url = request.GET.get('return_url')
    template_name='EcomApp1/login.html'
    context={}
    return render(request,template_name,context)

def logoutView(request):
    logout(request)
    request.session.clear()
    return redirect('login')

def cartView(request):
    try:
        if request.method == "POST":
            product = request.POST.get('product')
            remove = request.POST.get('remove')
            cart = request.session.get('cart')
            if cart:
                quantity = cart.get(product)
                if quantity:
                    if remove:
                        if quantity <= 1:
                            cart.pop(product)
                        else:
                            cart[product] = quantity - 1
                    else:
                        cart[product] = quantity + 1
                else:
                    cart[product] = 1
            else:
                cart = {}
                cart[product] = 1
            #   for check line if cart value in line no 104
            request.session['cart'] = cart
            return redirect('cart')
        # solution for Variable does Not Exists at failed lookup for key[cart]
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}
        ids = list(request.session.get('cart').keys())      #Error NoneType Attribute
        products = ProductModel.get_product_by_id(ids)
        template_name='EcomApp1/cart.html'
        context={'products':products}
        return render(request,template_name,context)

    except AttributeError:
        # return redirect('cart')
        message='Your Cart is Empty'
        template_name='EcomApp1/cart.html'
        context={'message':message}
        return render(request,template_name,context)

def checkoutView(request):
    if request.method == 'POST':
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        customer=request.session.get('cid')
        cart=request.session.get('cart')
        products=ProductModel.get_product_by_id(list(cart.keys()))
        for product in products:
            order=OrderModel(customer=CustomerModel(id=customer),product=product,
                             price=product.Price,address=address,
                             phone=phone,quantity=cart.get(str(product.id)))
            order.save()
            request.session['cart']={}
        return redirect('orders')

@auth_middleware
def ordersView(request):
    if request.method == 'GET':
        customer=request.session.get('cid')
        orders=OrderModel.get_order_by_cid(customer)
        return render(request,'EcomApp1/orders.html',{'orders':orders})

def updateprofileView(request):
    cobj=CustomerModel.objects.get(id=request.session.get('cid'))
    # print('cobj==',cobj)
    if request.method == "POST":
        fn = request.POST.get('fn')
        ln = request.POST.get('ln')
        pn = request.POST.get('pn')
        oldpw=request.POST.get('oldpw')
        newpw=request.POST.get('newpw')
        customer=CustomerModel.objects.get(id=request.session.get('cid'))
        if check_password(oldpw,customer.password):
            customer.password=newpw
            customer.password = make_password(customer.password)
            customer.first_name=fn
            customer.last_name=ln
            customer.phone = pn
            customer.save()
        else:
            messages.error(request,'Incorrect old passowrd')
            return redirect('update')
        return HttpResponse('Updated SuccessFully')
    # form= CustomerForm()
    template_name='EcomApp1/updateprofile.html'
    context={'cobj':cobj}
    return render(request,template_name, context)

# def placeorderView(request):
#     if request.method == 'POST':
#         # print('checkout.post',request.POST)
#         address=request.POST.get('address')
#         phone=request.POST.get('phone')
#         customer=request.session.get('cid')
#         cart=request.session.get('cart')
#         products=ProductModel.get_product_by_id(list(cart.keys()))
#         for product in products:
#             # print('cart id=',cart.get(str(product.id)))
#             order=OrderModel(customer=CustomerModel(id=customer),product=product,
#                              price=product.Price,address=address,
#                              phone=phone,quantity=cart.get(str(product.id)))
#             order.save()
#             request.session['cart']={}
#         return render(request,'EcomApp1/orders.html')
#     template_name='EcomApp1/placeorder.html'
#     context={}
#     return render(request,template_name, context)

def profileView(request):
    cid=request.session.get('cid')
    # print('cid=',cid)
    customerobj=CustomerModel.objects.get(id=cid)
    template_name='EcomApp1/profile.html'
    context={'customerobj':customerobj}
    return render(request,template_name,context)

# Paginator
def paginatorView(request):
    #Code For AddToCart
    if request.method == "POST":
        product=request.POST.get('product')
        remove=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity= cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart={}
            cart[product] = 1
        #   for check line if cart value in line no 104
        request.session['cart'] = cart
        return redirect('paginator')

    # code for cart error in pipe for men.html
    cart=request.session.get('cart')
    if not cart:
        request.session.cart={}

    products=None
    categories=CategoryModel.objects.all()

    #Code for price Filter
    CategoryId=request.GET.get('category')
    if CategoryId:
        products=ProductModel.get_products_by_categoryId(CategoryId)
    else:
        product=ProductModel.objects.all().order_by('id')
        paginator=Paginator(product,9)
        page_number=request.GET.get('page')
        products=paginator.get_page(page_number)

    productbyPrice=request.GET.get('productPrice')
    if productbyPrice == 'below500':
        products=ProductModel.objects.filter(Price__lte=500)
    elif productbyPrice == 'above501':
        products = ProductModel.objects.filter(Price__gte=500)

    brandbyname = request.GET.get('brandname')
    if brandbyname:
        products = ProductModel.objects.filter(Name=brandbyname)

    template_name='EcomApp1/paginator.html'
    context={'products':products,'categories':categories,'CategoryId':(CategoryId)}
    # return HttpResponse('Done')       # check error
    return render(request,template_name,context)


def resetpasswordView(request):
    if request.method == "POST":
        email=request.POST.get('email')
        print('email=', email)
        request.session['remail'] = email
        if not email:
            messages.error(request,'Email required')
            return redirect('resetpassword')
        customer=CustomerModel.objects.filter(email=email)
        if not customer:
            messages.error(request,'Enter Valid Email')
            return redirect('resetpassword')
        else:
            html_content = render_to_string("EcomApp1/email.html")
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                'Reset Password', #msg
                text_content,   #html page
                settings.EMAIL_HOST_USER,  #from
                [email],    #to
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            return HttpResponse('Reset Password link sent on your Email Account')
    template_name='EcomApp1/resetpassword.html'
    context={}
    return render(request,template_name,context)

def changepasswordView(request):
    remail = request.session.get('remail')
    if not remail:
        return redirect('resetpassword')

    if request.method == "POST":
        npw=request.POST.get('npw')
        cpw=request.POST.get('cpw')
        if npw == cpw:
            obj=CustomerModel.objects.get(email=remail)
            obj.password=npw
            obj.password=make_password(obj.password)
            obj.save()
            request.session.clear()
            return HttpResponse('Your Password is successFully Changed')
        else:
            messages.error(request,'Password Does not match')
            return redirect('changepassword')

    template_name='EcomApp1/changepassword.html'
    context={}
    return render(request,template_name,context)

# Code for invoice pdf
def render_pdf_view(request,i):
    order=OrderModel.objects.get(id=i)

    template_path = 'EcomApp1/pdf1.html'
    context = {'order':order}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    #if download pdf(force download)
    #response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    # if show pdf on browser
    response['Content-Disposition'] = ' filename="invoice.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    print('pisa',pisa_status)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response

# def searchView(request):
#     query=request.GET['query']
#     print('query=',query)
#     productsName=ProductModel.objects.filter(Name__icontains=query)
#     productsdescription=ProductModel.objects.filter(description__icontains=query)
#     products=productsName.union(productsdescription)
#     if not products:
#         template_name = 'EcomApp1/search.html'
#         messages.error(request,'No products with this name')
#         context = {'query': query}
#         return render(request, template_name,context)
#     template_name='EcomApp1/search.html'
#     context={'products':products}
#     return render(request,template_name,context)


def sendotpView(request):
    if request.method == "POST":
        email=request.POST.get('email')

        OTP = str(random.randint(1000, 9999))
        SOTP=request.session['SOTP']=OTP
        print('OTP',OTP)
        print('SOTP', SOTP)
        send_mail(
            'Signed-in ',  # Subject
            'Hello, I am  AJAY from All Shopping.com Email Verification for SignUp OTP-,' + OTP,  # msg
            settings.EMAIL_HOST_USER,  # From
            [email],  # To
            fail_silently=False,
        )
        return redirect('signup')
    tempate_name='EcomApp1/sendotp.html'
    return render(request,tempate_name)

def ajaxdataView(request):
    query=request.GET['q']
    print('query=',query)
    products=ProductModel.objects.filter(Name__icontains=query) #Roadstar
    if not products:
        template_name = 'EcomApp1/ajaxdata.html'
        messages.error(request,'No products with this name')
        context = {'query': query}
        return render(request, template_name,context)
    template_name='EcomApp1/ajaxdata.html'
    context={'products':products}
    return render(request,template_name,context)