"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views
app_name='shop'
urlpatterns = [
    path('',views.Categoryview.as_view(),name='categories'),
    path('product/<int:i>',views.Productview.as_view(),name='product'),
    path('pro/<int:i>',views.Detailview.as_view(),name='pro'),
    path('signup', views.Signup.as_view(), name='signup'),
    path('verify', views.Otpverification.as_view(), name='verify'),
    path('signin', views.Signin.as_view(), name='signin'),
    path('signout', views.Signout.as_view(), name='signout'),
    path('addcategory', views.Addcategoryview.as_view(), name='addcategory'),
    path('addproduct', views.Addproductview.as_view(), name='addproduct'),
]
