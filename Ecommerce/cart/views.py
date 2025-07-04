from django.shortcuts import render, redirect
from django.views import View
from shop.models import Product
from cart.models import Cart, Order_Items


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
                response_payment = client.order.create(dict(amount=total, currency='INR'))

                #prints the response_payment
                print(response_payment)

                order_id=response_payment['id']
                order_object.order_id=order_id
                order_object.is_ordered=True
                order_object.save()

            elif order_object.payment_method=='COD':
                order_object.is_ordered=True
                order_object.save()
            else:
                pass
            return render(request, 'payment.html')
