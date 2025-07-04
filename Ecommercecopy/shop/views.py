from django.shortcuts import render
from django.views import View
from shop.models import Category,Product
class Categoryview(View):
    def get(self,request):
        c=Category.objects.all()
        return render(request,'categories.html',{'cate':c})

class Productview(View):
    def get(self,requset,i):
        c=Category.objects.get(id=i)
        return render(requset,'product.html',{'category':c})

class Detailview(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        return render(request,'view_product.html',{'pro':p})