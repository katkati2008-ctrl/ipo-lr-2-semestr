from django.shortcuts import render

def hello_world(request):
    return render(request,'index.html')
# Create your views here.
