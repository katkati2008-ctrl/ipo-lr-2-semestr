from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Product, Category, Manufacturer, Cart, CartElement
def main(request):
    return render(request,'NewApp/index.html')

def author(content):
    content="""
<title>Об авторе</title>
<h1>Информация об авторе</h1>
    <ul>
        <h2>Автор: Мазалевская Екатерина</h2>
        <h2>Группа: 89 ТП</h2>
    </ul>"""
    return HttpResponse(content)

def about(content):
    content = """
    <title>О магазине</title>
    <h1>Здесь находится основная информация о магазине</h1>
    <ul>
       <h2>Данный сайт будет содержать ассортимент,состоящий из товаров для пикника<h2>
         </ul>"""
    return HttpResponse(content)

def product_list(request):
    products = Product.objects.all()
    category = Category.objects.all()
    manufacturer= Manufacturer.objects.all()
    
   
    categ = request.GET.get('category')
    if categ:
        products = products.filter(category_id=categ)
    
    manuf = request.GET.get('manufacturer')
    if manuf:
        products = products.filter(manufacturer_id=manuf)
    
    search = request.GET.get('search')
    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )
    return render(request, 'NewApp/product_list.html', {
        'products': products,
        'category': category,
        'manufacturer': manufacturer,
    })


def product_detail(request,pk):
   product = get_object_or_404(Product, pk=pk)
   return render(request, 'NewApp/product_detail.html', {'product': product})

@login_required
def add_to_cart(request,item_id):
    product = get_object_or_404(Product, pk=item_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartElement.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        if item.quantity < product.quantity:
            item.quantity += 1
            item.save()
            messages.success(request, 'Количество увеличено')
        else:
            messages.error(request, 'Нет в наличии')
    
    return redirect('cart_view')

@login_required
def update_cart(request,item_id):
    item = get_object_or_404(CartElement, pk=item_id, cart__user=request.user)
    if request.method == 'POST':
        new_qty = int(request.POST.get('quantity', 1))
        
        if new_qty <= 0:
            item.delete()
            messages.success(request, 'Товар удален')
        elif new_qty <= item.product.quantity:
            item.quantity = new_qty
            item.save()
            messages.success(request, 'Количество обновлено')

    return redirect('cart_view')

@login_required
def remove_from_cart(request,item_id):
    item = get_object_or_404(CartElement, pk=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, 'Товар удален')
    return redirect('cart_view')
    

@login_required
def cart_view(request):
   cart, _ = Cart.objects.get_or_create(user=request.user)
   return render(request, 'NewApp/cart.html', {'cart': cart})

@login_required
def checkout(request):
   cart, _ = Cart.objects.get_or_create(user=request.user)
    
# Create your views here.

