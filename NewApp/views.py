from django.shortcuts import render
from django.http import HttpResponse

def main(request):
    return render(request,'index.html')

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
# Create your views here.

