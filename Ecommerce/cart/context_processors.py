from cart.models import Cart
def count_items(request):
    if request.user.is_authenticated:
        u=request.user
        c=Cart.objects.filter(user=u)
        count=0
        for i in c:
            count=count+i.quantity
    else:
        count=0
    return {'count':count}