from shop.models import Category
def dropdown(request):
    c=Category.objects.all()
    return {'cat':c}