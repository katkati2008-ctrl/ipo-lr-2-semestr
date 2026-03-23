from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Product, Category, Manufacturer, Cart, CartElement,Order,OrderElement
from django.conf import settings
from openpyxl import Workbook
from io import BytesIO
from django.core.mail import EmailMessage
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from rest_framework import routers, serializers, viewsets


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
       <h2>Данный сайт представляет вещи для пикника и туризма<h2>
       <h2>С ассортиментом вы можете ознакомиться тут:<h2>
       <a href="/catalog/">Перейти в каталог</a>
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
   items = CartElement.objects.filter(cart=cart)
   
   if not items:
       messages.error(request,"Корзина пуста")
       return redirect('cart_view')
   
   if request.method == 'POST':
    
       home_address=request.POST.get('home_address')
       num_phone=request.POST.get('num_phone')
       user_email = request.POST.get('email')

       if not user_email:
            user_email = request.user.email

       if not user_email:
            messages.error(request, "Укажите email для получения чека")
            return render(request, 'NewApp/checkout.html', {
                'items': items, 
                'total_price': sum(i.elem_price() for i in items)})

       if not home_address or not num_phone:
           messages.error(request,"Введите все запрашиваемые данные")
           return render(request,'NewApp/checkout.html',{'items':items})
    
       total_price= sum(item.elem_price() for item in items)

       order=Order.objects.create(
           user=request.user,
           home_address=home_address,
           num_phone=num_phone,
           email=user_email, 
           total_price=total_price
       )
       
       for item in items:
           OrderElement.objects.create(
               order=order,
               product=item.product,
               quantity=item.quantity,
               price=item.product.price
           )
        
       wb = Workbook()
       ws = wb.active
       ws.title = f"Заказ_{order.id}"
       ws.append(["Товар","Количество","Цена за шт.","Сумма"])
       for item in items:
           ws.append([
               item.product.name,
               item.quantity,
               item.product.price,
               item.elem_price()
           ])
           product=item.product
           product.quantity-=item.quantity
           product.save()
       ws.append([])
       ws.append(["Сумма заказа:",total_price])

       excel_file = BytesIO()
       wb.save(excel_file)
       excel_file.seek(0)


       subject = f"Ваш заказ #{order.id} оформлен"
       message=f'''
       Ваш заказ успешно оформлен.
       Номер заказа: {order.id}.
       Чек будет отправлен на вашу почту.
       Спасибо за покупку!
       '''

       from_email = settings.DEFAULT_FROM_EMAIL
      
       email = EmailMessage(
            subject,
            message,
            from_email,
            [user_email]
        )
       email.attach(f"check_{order.id}.xlsx",excel_file.getvalue(),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')  
       email.send(fail_silently=False)
       items.delete()
     
       return redirect('cart_view')
   
   context = {
        'items':items,
        'total_price':sum(item.elem_price() for item in items)
    }
    
   return render(request,'NewApp/checkout.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('product_list')
    else:
        form = CustomUserCreationForm()
    return render(request,'registration/register.html', {'form': form})

class API_ViewSet(viewsets.ModelViewSet):
    pass


# Create your views here.

