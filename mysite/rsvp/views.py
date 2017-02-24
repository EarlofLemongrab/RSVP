from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import  render_to_response  
from django.template import  RequestContext  
from django.http import HttpResponseRedirect  
from django.contrib.auth.models import User 
from django.contrib import auth  
from models import *  
 
def index(req):   
    username=req.session.get('username', '')  
    content = {'active_menu': 'homepage', 'user': username}  
    return render_to_response('index.html', content)
 
def regist(req):  
    if req.session.get('username', ''):  
         return HttpResponseRedirect('/')  
    status=""  
    if req.POST:  
        username = req.POST.get("username","")  
        if User.objects.filter(username=username):  
            status = "user_exist"  
        else:  
            password=req.POST.get("password","")  
            repassword = req.POST.get("repassword","")  
            if password!=repassword:  
                status = "re_err"  
            else:  
                newuser=User.objects.create_user(username=username,password=password)  
                newuser.save()                               
                new_myuser = MyUser(user=newuser,phone=req.POST.get("phone"))      
                new_myuser.save()  
                status = "success"  
                return HttpResponseRedirect("/login/")  
    return render(req,"regist.html",{"active_menu":"hompage","status":status,"user":""})  
  
def login(req):  
    if req.session.get('username', ''):  
        return HttpResponseRedirect('/')  
    status=""  
    if req.POST:  
        username=req.POST.get("username","")  
        password=req.POST.get("password","")  
        user = auth.authenticate(username=username,password=password)   
        if user is not None:  
                auth.login(req,user)          
                req.session["username"]=username      
                return HttpResponseRedirect('/')  
        else:  
            status="not_exist_or_passwd_err"  
    return render(req,"login.html",{"status":status})  

def logout(req):  
    auth.logout(req)  
    return HttpResponseRedirect('/')  

def get_acad_list():  
    room_list = ConfeRoom.objects.all() 
    acad_list = set()  
    for room in room_list:  
        acad_list.add(room.acad)  
    return list(acad_list)  

def viewroom(req):  
    username = req.session.get('username', '')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  
    acad_list=get_acad_list()   
    room_acad = req.GET.get("acad","all")                                           
    if room_acad not in acad_list:          
        room_acad = "all"  
        room_list=ConfeRoom.objects.all()  
    else:  
        room_list=ConfeRoom.objects.filter(acad=room_acad)  
    content = {"active_menu":'viewroom',"acad_list":acad_list,"room_acad":room_acad,"room_list":room_list,"user":user}  
    return render(req,'viewroom.html',content)  
 
def detail(req):  
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  
    Id = req.GET.get("id","") 
    req.session["id"]=Id  
    if Id == "":  
        return HttpResponseRedirect('/viewroom/')  
    try:  
        room = ConfeRoom.objects.get(pk=Id) 
        ro =Detail.objects.get(pk=Id)  
    except:               
        return HttpResponseRedirect('/viewroom/')  
    img_list = Detail.objects.filter(room=room)  
    num_list = get_order_list()  
    if room.num not in num_list:    
        or_sta="yes"  
    else:  
        or_sta="no"  
    content = {"active_menu":"viewroom","room":room,"img_list":img_list,"ro":ro,"or_sta":or_sta,"user":user}  
    return render(req,'detail.html',content)  

 
def get_order_list():  
    num_list=set()  
    order_list=Order.objects.all()  
    for order in order_list:  
        num_list.add(order.num)  
    return list(num_list)  
def order(req):  
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  
    roid = req.session.get("id","")                   
    room = ConfeRoom.objects.get(pk=roid)  
    time = Detail.objects.get(name=room.name)  
    u = MyUser.objects.get(user__username=username)  
    order = Order(user=username,num=room.num,name=room.name,time=time.time,size=room.size,phone=u.phone)  
    order.save()  
    return render(req,"index2.html",{"user":user})  
    
def myorder(req):  
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  
    try:  
        my_order=Order.objects.all()        
        us_sta = "no"  
        return render(req,"myorder.html",{"myorder":my_order,"us_sta":us_sta,"user":user})  
                  
    except:  
        us_sta = "yes"        
        return render(req,"myorder.html",{"us_sta":us_sta,"user":user})  
       
def cancel(req):  
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  
    Id = req.GET.get("id","")      
    room =Order.objects.get(pk=Id)  
    room.delete()  
    return render(req,"index.html") 