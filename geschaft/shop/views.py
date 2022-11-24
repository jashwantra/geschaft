from django.shortcuts import render
from django.http import HttpResponse
from .models import product,contact,Orders
from math import ceil
import random

# Create your views here.
def index(request):
    allProds = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False
    
def search(request):
    query=request.GET.get('search')
    #print(query)
    allProds = []
    catprods = product.objects.values('category')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0:
        params={'msg':"Nothing found. Please try again with another keyword."}
    #print(params)
    return render(request,"shop/search.html",params)

def about(request):
    return render(request,"shop/about.html")

def Contact(request):
    if request.method=="POST":
        nam=request.POST.get('name','')
        emai=request.POST.get('email','')
        phon=request.POST.get('phone','')
        des=request.POST.get('desc','')
        #print(nam,emai,phon,des)
        cntct=contact(name=nam,email=emai,phone=phon,desc=des)
        cntct.save()
        thank=True
        return render(request,"shop/contact.html",{'thank':True})
    return render(request,"shop/contact.html")

def special(request):
    id = product.objects.values('id')
    x = random.randint(0, len(id)-1)
    prod=product.objects.filter(id=id[x]['id'])
    #print(prod)
    return render(request,"shop/special.html",{'product':prod[0],'id':id[x]['id']})

def prodview(request,myid):
    #Fetch the product using ID
    prdct = product.objects.filter(id=myid)
    #print(prdct[0].product_name)
    return render(request,"shop/productview.html",{'product':prdct[0],'id':myid})

def checkout(request):
    if request.method=="POST":
        itemjson=request.POST.get('itemjson','')
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        address=request.POST.get('address1','')+' '+request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip=request.POST.get('zip','')
        phone=request.POST.get('phone','')
        amount=request.POST.get('amount','')
        #print(nam,emai,phon,des)
        order=Orders(items_json=itemjson,name=name,email=email,address=address,city=city,state=state,zip_code=zip,phone=phone,amount=amount)
        order.save()
        thank=True
        id=order.order_id
        return render(request,"shop/checkout.html",{'thank':thank,'id':id})
    return render(request,"shop/checkout.html")