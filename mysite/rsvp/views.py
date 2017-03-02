from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import  render_to_response  
from django.template import  RequestContext  
from django.http import HttpResponseRedirect  
from django.contrib.auth.models import User 
from django.contrib import auth  
from models import *  
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.conf import settings
import json
 
def index(req):   
    username=req.session.get('username', '')  
    content = {'user': username}  
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
                new_myuser = MyUser(user=newuser,email=req.POST.get("email"),name = username)      
                new_myuser.save()  
                status = "success"  
                return HttpResponseRedirect("/rsvp/login/")  
    return render(req,"regist.html",{"status":status,"user":""})  
  
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
                return HttpResponseRedirect('/rsvp/')  
        else:  
            status="not_exist_or_passwd_err"  
    return render(req,"login.html",{"status":status}) 
     
@login_required
def logout(req):  
    auth.logout(req)  
    return HttpResponseRedirect('/rsvp/')  

@login_required
def events(req):
    username = req.session.get('username','')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''

    try:
        owner_events = Event.objects.filter(owners__user__name = username)
        vendor_events = Event.objects.filter(vendors__user__name = username)
        guest_events = Event.objects.filter(guests__user__name = username)
        us_sta = "no"  
        return render(req,"events.html",{"owner_events":owner_events,"vendor_events":vendor_events,"guest_events":guest_events,"us_sta":us_sta,"user":user})  
                  
    except:  
        us_sta = "yes"        
        return render(req,"events.html",{"us_sta":us_sta,"user":user})

@login_required
def ownerdetails(req):
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  
    Id = req.GET.get("id","") 
    req.session["id"]=Id    
    try:  
        event = Event.objects.get(pk=Id) 
    except:               
        return HttpResponseRedirect('/rsvp/events/')    
    content = {"event":event,"user":user}  
    return render(req,'ownerdetails.html',content)


@login_required
def create(req):
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''                     
    if req.POST:
        plusone = req.POST.get("plusone","")
        try:
            o = Owner.objects.get(user=user) 
        except:
            o = Owner(user=user)
            o.save()
        name = req.POST.get("eventname","")
        date = req.POST.get("date","") 
        event = Event(name=name,date=date)
        event.plusone = plusone
        event.save()
        event.owners.add(o)
        return  HttpResponseRedirect("/rsvp/events/")
    
    return render(req,"create.html",{})

@login_required
def edit(req):
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  

    Id = req.GET.get("id","") 
    req.session["id"]=Id    

    try:  
        event = Event.objects.get(pk=Id) 
        owners = event.owners.all()
        vendors = event.vendors.all()
        guests = event.guests.all()
        textquestions = event.textquestion_set.all()
        choicequestions = event.choicequestion_set.all()
        plusone = event.plusone
    except:               
        return HttpResponseRedirect('/rsvp/events/')    
    
    content = {"event":event,"user":user,"owners":owners,"vendors":vendors,"guests":guests,"textquestions":textquestions,"choicequestions":choicequestions,"plusone" : plusone}  
    return render(req,'edit.html',content)

@login_required
def add(req):
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''                     
    
    Id = req.GET.get("id","") 
    req.session["id"]=Id   

    if Id == "":
        return HttpResponseRedirect('/rsvp/events/')
    event = Event.objects.get(pk=Id)

    if req.POST:
        add_owner = req.POST.get("ownername","")
        add_vendor = req.POST.get("vendorname","")
        add_guest = req.POST.get("guestname","")
        plusone = req.POST.get("plusone","")
        text_question = req.POST.get("textquestion","")
        choice_question =req.POST.get("choicequestion","")

        if str(plusone) == 'on':
            event.plusone = True
        else:
            event.plusone = False
        event.save()
        if add_owner!="":
            try:  
                u1 = MyUser.objects.get(name=add_owner)
                try:
                    o = Owner.objects.get(user__name=add_owner)
                except Owner.DoesNotExist:
                    u = MyUser.objects.get(name=add_owner)
                    o = Owner(user=u)  
                    o.save()
                    event.owners.add(o)
            except  MyUser.DoesNotexist:
                print "no user"
                return  HttpResponseRedirect("/rsvp/add/")
        if add_vendor!="":
            try:    
                u2 = MyUser.objects.get(name=add_vendor)
                print "added vendor "+u2.name
                try:
                    v = Vendor.objects.get(user__name=add_vendor)
                    print "has vendor "+v.user.name
                except Vendor.DoesNotExist:
                    u = MyUser.objects.get(name=add_vendor)
                    v = Vendor(user=u2)
                    v.save()
                    event.vendors.add(v)
            except  MyUser.DoesNotExist:
                return  HttpResponseRedirect("/rsvp/add/")
        if add_guest!="":    
            try:
                u3 = MyUser.objects.get(name=add_guest)            
                try:
                    g = Guest.objects.get(user__name=add_guest)
                except Guest.DoesNotExist:
                    u = MyUser.objects.get(name=add_guest)
                    g = Guest(user=u)
                    g.save()
                    event.guests.add(g)
            except  MyUser.DoesNotExist:
                return  HttpResponseRedirect("/rsvp/add/")
        if text_question!="":
            tq = TextQuestion(event = event,question_text = text_question,finalized = False)
            tq.save()
        if choice_question!="":
            cq = ChoiceQuestion(event = event,question_text = choice_question,finalized = False)
            cq.save()

        
        return  HttpResponseRedirect("/rsvp/events/")
    
    return render(req,"add.html",{})

@login_required
def addq(req):
    username = req.session.get('username','')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
    Id = req.GET.get("id","") 
    req.session["id"]=Id  
    if Id == "":  
        return HttpResponseRedirect('/rsvp/events/')  
    if req.POST:
        question_text = req.POST.get("question_text","")
        event = Event.objects.get(pk=Id)
        q = TextQuestion(event=event,question_text=question_text)
        q.save()
        response_data = {}
        response_data['result'] = 'Create question successful'
        response_data['question_id'] = q.pk
        response_data['text'] = q.question_text
        response_data['author'] = username
        return HttpResponse(
            json.dumps(response_data),
            content_type = "application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isnt happening"}),
            content_type = "application/json"
        )

@login_required
def guestdetails(req):
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  

    Id = req.GET.get("id","") 
    req.session["id"]=Id    

    #try:  
    event = Event.objects.get(pk=Id) 
    textquestions = event.textquestion_set.all()
    choicequestions = event.choicequestion_set.all()
    choiceresponse = []
    textresponse = []
    for textquestion in textquestions:
        textresponse.append(textquestion.textresponse_set.filter(username=username))
    for choicequestion in choicequestions:
        choiceresponse.append(choicequestion.choice_set.filter(choiceresponse__username=username))
    print(choiceresponse)
    #except:               
    #    return HttpResponseRedirect('/rsvp/events/')    
    
    content = {"event":event,"user":user,"textquestions":textquestions,"choicequestions":choicequestions,"textresponse":textresponse,"choiceresponse":choiceresponse}  
    return render(req,'guestdetails.html',content)


@login_required
def vendordetails(req):
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  

    Id = req.GET.get("id","")
    req.session["id"]=Id

    try:  
        event = Event.objects.get(pk=Id) 
        choicequestions = event.choicequestion_set.filter(vendors__user__name=username)
        textquestions = event.textquestion_set.filter(vendors__user__name=username)
    except:               
        return HttpResponseRedirect('/rsvp/events/')    
    
    content = {"event":event,"choicequestions":choicequestions,"textquestions":textquestions}  
    return render(req,'vendordetails.html',content)

@login_required
def textfinalized(req):

    Id = req.GET.get("id","")
    req.session["id"]=Id

    try:  
        t = TextQuestion.objects.get(pk=Id) 
        t.finalized = True
        t.save()
    except:               
        return HttpResponseRedirect('/rsvp/events/')   

    print(t.finalized)
    return HttpResponseRedirect('/rsvp/events/')

@login_required
def choicefinalized(req):
    Id = req.GET.get("id","")
    req.session["id"]=Id

    try:  
        t = ChoiceQuestion.objects.get(pk=Id) 
        t.finalized = True
        t.save()
    except:               
        return HttpResponseRedirect('/rsvp/events/')   

    print(t.finalized)
    return HttpResponseRedirect('/rsvp/events/')  

@login_required
def addtextvendor(req):
    Id = req.GET.get("id","")
    req.session["id"]=Id                     
    q = TextQuestion.objects.get(pk = Id)
    if req.POST:
        username = req.POST.get("name","")
        u = MyUser.objects.get(name = username)
        
        try:
            v = Vendor.objects.get(user = u)
        except:
            v = Vendor(user=u)
            v.save()
        
        q.vendors.add(v)
        q.save()
        
        return  HttpResponseRedirect("/rsvp/events/")
    return  render(req,"addtextvendor.html",{})
    #return render(req,'addtextvendor.html',content)       
@login_required
def addchoicevendor(req):
    Id = req.GET.get("id","")
    req.session["id"]=Id                     
    q = ChoiceQuestion.objects.get(pk = Id)
    if req.POST:
        username = req.POST.get("name","")
        u = MyUser.objects.get(name = username)
        
        try:
            v = Vendor.objects.get(user = u)
        except:
            v = Vendor(user=u)
            v.save()
        
        q.vendors.add(v)
        q.save()
        
        return  HttpResponseRedirect("/rsvp/events/")
    return  render(req,"addchoicevendor.html",{})

@login_required
def edittextresponse(req):

    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  

    Id = req.GET.get("id","")
    req.session["id"]=Id
    q = TextQuestion.objects.get(pk = Id)

    if q.finalized == True:
        return HttpResponseRedirect("/rsvp/events/")

    if req.POST:
        new_response_text = req.POST.get("name","")
        
        query_set = q.textresponse_set.filter(username=username)
        if query_set.count() > 0:
            old_response = query_set.get(username=username)
            old_response.response_text = new_response_text
            old_response.save()
        else:
            inserted_response = TextResponse(question = q,response_text=new_response_text,username=username)
            inserted_response.save()
            q.textresponse_set.add(inserted_response)
            q.save()     
        return  render(req,"edittextresponse.html",{"q" : q})

    return  render(req,"edittextresponse.html",{"q" : q})

@login_required
def editchoiceresponse(req):

    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  

    Id = req.GET.get("id","")
    req.session["id"]=Id
    q = ChoiceQuestion.objects.get(pk = Id)

    if req.POST:
        new_choice_text = req.POST.get("name","")
        query_set = q.choice_set.filter(choiceresponse__username=username)

        if query_set.count() > 0:
            old_choice = query_set.first()
            old_response = old_choice.choiceresponse_set.filter(username=username)
            print(old_response.first())
            old_response.first().delete()
            new_Choice = Choice.objects.filter(choice_text=new_choice_text)
            old_choice2 = ChoiceResponse(user_choice = new_Choice.first(), username=username)
            old_choice2.save()

        else:
            #new_Choice = Choice(question = q,choice_text = new_choice_text)
            new_Choice = Choice.objects.filter(choice_text=new_choice_text).first()
            inserted_response = ChoiceResponse(user_choice = new_Choice,username=username)
            inserted_response.save()
            ##query_set.add(inserted_response)
            ##query_set.save()            

        return  render(req,"editchoiceresponse.html",{"q":q})

    return  render(req,"editchoiceresponse.html",{"q":q})


@login_required
def textquestiondetails(req):
    Id = req.GET.get("id","")
    req.session["id"]=Id
    q = TextQuestion.objects.get(pk = Id)

    text_responses = q.textresponse_set.all()
    content = {"q" : q, "textresponses" : text_responses}
    return render(req,"textquestiondetails.html",content)




@login_required
def choicequestiondetails(req):
    Id = req.GET.get("id","")
    req.session["id"]=Id
    q = ChoiceQuestion.objects.get(pk = Id)
    choices = q.choice_set.all()
    choiceresponses = []

    for c in choices:
        for d in ChoiceResponse.objects.filter(user_choice=c):
            choiceresponses.append(d)

    #print(choiceresponses)
    content = {"q" : q, "choiceresponses" : choiceresponses}
    return render(req,"choicequestiondetails.html",content)  

@login_required
def addchoice(req):
    Id = req.GET.get("id","")
    req.session["id"]=Id
    q = ChoiceQuestion.objects.get(pk = Id)
    choices = q.choice_set

    if req.POST:
        new_choice_text = req.POST.get("name","")
        new_choice = Choice(question=q,choice_text = new_choice_text)
        new_choice.save()
        choices.add(new_choice)

    return render(req,"addchoice.html",{"choices":choices,"q":q})
def textquestionedit(req):
    username = req.session.get('username','')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
        
    Id = req.GET.get("id","")
    req.session["id"]=Id
    q = TextQuestion.objects.get(pk = Id)
    event = q.event
    print event
    guest_set = event.guests.all()
    print guest_set
    for g in guest_set:
        my_u = g.user
        email = my_u.email
        print "Sending to "+email
        
        send_mail(
                'Your Answer of a reserved Event in ERSS RSVP might changed',
                'Please go to check',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
    if req.POST:
        new_question_text = req.POST.get("name","")
            
        q.question_text = new_question_text
        q.save()
        return  render(req,"textquestionedit.html",{"q" : q})
    return  render(req,"textquestionedit.html",{"q" : q})

def choicequestionedit(req):
    username = req.session.get('username','')
    if username != '':
        user = MyUser.objects.get(user__username=username)
    else:
        user = ''
        
    Id = req.GET.get("id","")
    req.session["id"]=Id
    q = ChoiceQuestion.objects.get(pk = Id)
    event = q.event
    guest_set = event.guests.all()
    print guest_set
    for g in guest_set:
        my_u = g.user
        email = my_u.email
        print "Sending to "+email
        
        send_mail(
            'Your Answer of a reserved Event in ERSS RSVP might changed',
            'Please go to check',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
    if req.POST:
        new_question_text = req.POST.get("name","")
        
        q.question_text = new_question_text
        q.save()
        return  render(req,"choicequestionedit.html",{"q" : q})
    return  render(req,"choicequestionedit.html",{"q" : q})




"""
@login_required
def addquestion(req):
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''                     
    
    Id = req.GET.get("id","") 
    req.session["id"]=Id

    event = Event.objects.get(pk=Id)   

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
    content = {"acad_list":acad_list,"room_acad":room_acad,"room_list":room_list,"user":user}  
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
    content = {"room":room,"img_list":img_list,"ro":ro,"or_sta":or_sta,"user":user}  
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
"""
