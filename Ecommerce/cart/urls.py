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
from django.urls import path,include
from cart import views
app_name='cart'
urlpatterns = [
      path('addtocart/<int:i>/',views.AddtoCartview.as_view(),name='addtocart'),
      path('cartview',views.Cartview.as_view(),name='cartview'),
     path('minus/<int:i>/', views.Minusview.as_view(), name='minus'),
    path('remove/<int:i>/', views.Removeview.as_view(), name='remove'),
    path('orderform',views.OrderFormView.as_view(),name='orderform'),
    path('success/<i>',views.SuccessView.as_view(),name='success'),
    path('your_order', views.Your_Orders.as_view(), name='your_order'),
]
from django.conf.urls.static import static
from django.conf import settings
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)