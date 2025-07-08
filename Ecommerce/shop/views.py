from django.shortcuts import render, redirect
from django.views import View
from shop.models import Category, Product
from shop.forms import SignupForm
from shop.forms import LoginForm,CategoryForm,ProductForm
from django.contrib.auth import authenticate, login, logout


class Categoryview(View):
    def get(self, request):
        c = Category.objects.all()
        return render(request, 'categories.html', {'cate': c})


class Productview(View):
    def get(self, requset, i):
        c = Category.objects.get(id=i)
        return render(requset, 'product.html', {'category': c})


class Detailview(View):
    def get(self, request, i):
        p = Product.objects.get(id=i)
        return render(request, 'view_product.html', {'pro': p})


from django.core.mail import send_mail


class Signup(View):
    def post(self, request):
        form_instance = SignupForm(request.POST)
        if form_instance.is_valid():
            user = form_instance.save(commit=False)
            user.is_active = False
            user.save()
            user.generate_otp()
            send_mail(
                "Ecommerce",
                user.otp,
                "ramprakashkp048@gmail.com",
                [user.email],
                fail_silently=False,
            )
            return redirect('shop:verify')
        return render(request, 'signup.html', {'form': form_instance})

    def get(self, request):
        form_instance = SignupForm
        return render(request, 'signup.html', {'form': form_instance})


from shop.models import User
from django.contrib import messages


class Otpverification(View):
    def post(self, request):
        o = request.POST['otp']
        try:
            u = User.objects.get(otp=o)
            u.is_active = True
            u.is_verified = True
            u.otp = None
            u.save()
            return redirect('shop:categories')
        except:
            # print('Invalid OTP')
            messages.error(request, 'Invalid OTP')
            return redirect('shop:verify')

    def get(self, request):
        return render(request, 'otp_verification.html')


class Signin(View):
    def post(self, request):
        form_instance = LoginForm(request.POST)
        if form_instance.is_valid():
            name = form_instance.cleaned_data['username']
            pwd = form_instance.cleaned_data['password']
            # user=User.objects.get(username=name)
            # print(name,pwd)
            user = authenticate(username=name, password=pwd)
            # authenticate() returns user object if all the user credentials are correct, else none
            if user and user.is_superuser == True:
                login(request, user)
                return redirect('shop:categories')

            elif user and user.is_superuser == False:
                login(request, user)
                return redirect('shop:categories')

            else:
                form_instance = LoginForm()
                return render(request, 'signin.html', {'form': form_instance})

    def get(self, request):
        form_instance = LoginForm()
        return render(request, 'signin.html', {'form': form_instance})


class Signout(View):
    def get(self, request):
        logout(request)
        return redirect('shop:signin')
class Addcategoryview(View):
    def get(self,request):
        form_instance=CategoryForm()
        return render(request,'addcategory.html',{'form':form_instance})
    def post(self,request):
        form_instance=CategoryForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')
        else:
            form_instance=CategoryForm()
            return render(request,'addcategory.html',{'form':form_instance})

class Addproductview(View):
    def get(self,request):
        form_instance=ProductForm()
        return render(request,'addproduct.html',{'form':form_instance})
    def post(self,request):
        form_instance=ProductForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')
        return render(request,'addproduct.html',{'form':form_instance})

# from django.db.models import Q
# class Search(View):
#     def get(self,request):
#         return render(request,'search.html')
#     def post(self,request):
#         data=request.POST['s']
#         p=Product.objects.filter(Q(category__name__icontains=data)|Q(name__icontains=data))
#         return render(request,'search.html',{'search':p})

from django.db.models import Q
class Search(View):
    def get(self,request):
        return render(request,'search.html')
    def post(self,request):
        data = request.POST['s']
        p = Product.objects.filter(Q(name__icontains=data)|Q(category__name__icontains=data))
        if p:
            return render(request, 'search.html', {'pro': p})
        else:
            messages.error(request, 'No Such Products')
            return render(request, 'search.html')

