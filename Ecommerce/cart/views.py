from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from shop.models import Product,User
from cart.models import Cart, Order_Items,Order
from django.contrib import messages
class AddtoCartview(View):
    def get(self, request, i):
        u = request.user
        p = Product.objects.get(id=i)
        try:
            c = Cart.objects.get(user=u, product=p)
            c.quantity += 1
            c.save()
        except:
            c = Cart.objects.create(user=u, product=p, quantity=1)
            c.save()

        return redirect('cart:cartview')


class Cartview(View):
    def get(self, request):
        u = request.user
        c = Cart.objects.filter(user=u)
        total = 0
        for i in c:
            total += i.quantity * i.product.price
        return render(request, 'cart.html', {'cart': c, 'total': total})


class Minusview(View):
    def get(self, request, i):
        u = request.user
        p = Product.objects.get(id=i)
        try:
            c = Cart.objects.get(user=u, product=p)
            if c.quantity > 1:
                c.quantity -= 1
                c.save()
            else:
                c.delete()
        except:
            pass

        return redirect('cart:cartview')


class Removeview(View):
    def get(self, request, i):
        u = request.user
        p = Product.objects.get(id=i)
        try:
            c = Cart.objects.get(user=u, product=p)
            c.delete()
        except:
            pass

        return redirect('cart:cartview')


import razorpay
from cart.forms import OrderForm
def check_stock(c):
    stock=True
    for i in  c:
        if i.product.stock<i.quantity:
            stock=False
            break
    return stock

class OrderFormView(View):
    def get(self, request):
        form_instance = OrderForm()
        return render(request, 'order_form.html', {'form': form_instance})

    def post(self, request):
        form_instance = OrderForm(request.POST)
        u = request.user
        if form_instance.is_valid():
            order_object = form_instance.save(commit=False)
            order_object.user = u
            order_object.save()  #creates an order_object in order table
            c = Cart.objects.filter(user=u)  #cart items selected by particular user
            stock=check_stock(c) #to check the stock before creating order
            if stock:

                for i in c:
                    o = Order_Items.objects.create(order=order_object, product=i.product, quantity=i.quantity)
                    o.save()
                    # in each iteration creates order_items object corresponding to a cart object
                #order amount
                total = 0
                for i in c:
                    total += i.quantity * i.product.price

                if order_object.payment_method=='ONLINE':
                    #Razorpay Payment Gateway Integration
                    #1.creates client connection
                    client = razorpay.Client(auth=('rzp_test_ihbpqbypZmzn9g', '057NThFTOGvUx4rFmERmGEvR'))

                    #2.order creation
                    response_payment = client.order.create(dict(amount=total*100, currency='INR'))

                    #prints the response_payment
                    print(response_payment)

                    order_id=response_payment['id']
                    order_object.order_id=order_id
                    order_object.is_ordered=False
                    order_object.amount=total
                    order_object.save()
                    return render(request, 'payment.html', {'payment': response_payment, 'name': u.username})

                elif order_object.payment_method=='COD':
                    order_object.is_ordered=True
                    order_object.amount = total
                    order_object.save()
                    items = Order_Items.objects.filter(order=order_object)
                    for i in items:
                        i.product.stock -= i.quantity
                        i.product.save()
                    c = Cart.objects.filter(user=u)
                    c.delete()
                    return redirect('shop:categories')

                else:
                    pass

            else:
                 messages.error(request,'Currently Items Not Available')
                 return render(request,'payment.html',)

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
@method_decorator(csrf_exempt,name='dispatch')
class SuccessView(View):
    def post(self,request,i):
        user=User.objects.get(username=i)
        login(request,user)

        response=request.POST
        print(response)

        o=Order.objects.get(order_id=response['razorpay_order_id'])
        o.is_ordered=True
        o.save()

        items=Order_Items.objects.filter(order=o)
        for i in items:
            i.product.stock-=i.quantity
            i.product.save()

        c=Cart.objects.filter(user=user)
        c.delete()
        return render(request,'success.html')

class Your_Orders(View):
    def get(self,request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        return render(request,'your_order.html',{'orders':o})