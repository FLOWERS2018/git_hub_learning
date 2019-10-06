from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html")


def customer_list(request):
    return render(request, "sales/customers.html")


def tpl1(request):
    user_list = [1,2,3,4]
    return render(request, 'tpl1.html',{'u':user_list})



def tpl2(request):
    name = 'root'
    return render(request,'tpl2.html',{'name':name})


def tpl3(request):
    status = "已删除"
    return render(request,'tpl3.html',{'status':status})


def tpl4(request):
    name="GFDKjjkljkjGHj"
    return render(request,'tpl4.html',{"name":name})