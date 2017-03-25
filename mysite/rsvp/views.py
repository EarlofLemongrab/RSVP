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
import requests
import argparse
import json
import pprint
import sys
import urllib
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode
import json

CLIENT_ID = "0-WYOJnzv9VGXlo2bjh-Mg"
CLIENT_SECRET = "ir5CSXJg9a6o4hXO3QTElzuIklVPz6WbczG2x8QrviJZuCAsyhzn3Jf78JGWEFeG"

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'
SEARCH_LIMIT = 3

#Load index page 
def index(req):   
    username=req.session.get('username', '')  
    content = {'user': username}  
    return render_to_response('index.html', content)

#Handles user registration; read in username, password, repassword, email to create MyUser instance and user instance from django auth.
def regist(req):  
    if req.session.get('username', ''):  
         return HttpResponseRedirect('/rsvp/index.html')  
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

#handles user login; Be aware that we use POST method to ensure data is transmitted in a secure way  
def login(req):  
    if req.session.get('username', ''):  
        return HttpResponseRedirect('/rsvp/')  
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

#hanles user logout     
@login_required
def logout(req):  
    auth.logout(req)  
    return HttpResponseRedirect('/rsvp/')  


# Display event list by selecting user relevant events by user's Owner, Vendor, Guest instance respectively.
# @login_required can provide session protection
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

# Display what owner should see
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

# Start a new event
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
        print event.plusone
        if(event.plusone == True):
            event.plusone = True
        else:
            event.plusone = False
        event.save()
        event.owners.add(o)
        return  HttpResponseRedirect("/rsvp/events/")
    
    return render(req,"create.html",{})

# Display editable fields
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

# Edit an event: this function can handle all editing of an event at the same time 
# by taking in multiple parameters like owner_to_be_added as well as question to be added.
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
                    event.owners.add(o)
                except Owner.DoesNotExist:
                    u = MyUser.objects.get(name=add_owner)
                    o = Owner(user=u)  
                    o.save()
                    event.owners.add(o)
            except  MyUser.DoesNotExist:
                print "no user"
                return  HttpResponseRedirect("/rsvp/add/")
        if add_vendor!="":
            try:    
                u2 = MyUser.objects.get(name=add_vendor)
                print "added vendor "+u2.name
                try:
                    v = Vendor.objects.get(user__name=add_vendor)
                    event.vendors.add(v)
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
                    event.guests.add(g)
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

# Deprecated
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

# Display choice and text questions for guest view by quiring with guest id
@login_required
def guestdetails(req):
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  

    Id = req.GET.get("id","") 
    req.session["id"]=Id    
  
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

    content = {"event":event,"user":user,"textquestions":textquestions,"choicequestions":choicequestions,"textresponse":textresponse,"choiceresponse":choiceresponse}  
    return render(req,'guestdetails.html',content)

# Display questions vendor allowed to see; each vendor may see different questions
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

# set text question finalized
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

# set choice question finalized
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

# allow a vendor to see a text question by adding vendor instance id to allowed list of a text question
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

#similar to above one
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

# read user's new response to text question and update
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


#   read user's new choice response and update database
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

# display responses to a specific text question
@login_required
def textquestiondetails(req):
    Id = req.GET.get("id","")
    req.session["id"]=Id
    q = TextQuestion.objects.get(pk = Id)

    text_responses = q.textresponse_set.all()
    content = {"q" : q, "textresponses" : text_responses}
    return render(req,"textquestiondetails.html",content)



# display responses to a choice question
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


# Add choice to one choice question
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

# allow text question to be edited and send email
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

# allow choice question to be changed and send email 
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



def sendmessage(req):
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''  
    if req.POST:
        receiver = req.POST.get("receiver","")
        u = MyUser.objects.get(name = receiver)
        subtitle = req.POST.get("subtitle","")
        content = req.POST.get("content","")
        m = Msg(sender = user,receiver=u,subtitle=subtitle,content=content)
        m.save()
        
        return  HttpResponseRedirect("/rsvp/events/")
    return  render(req,"sendmessage.html",{})


def inbox(req):
    username = req.session.get('username','')  
    if username != '':  
        user = MyUser.objects.get(user__username=username)  
    else:  
        user = ''    
    msgs = Msg.objects.filter(receiver=user)
    
        

    return render(req,"inbox.html",{"msgs":msgs})

def obtain_bearer_token(host, path):
    """Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        str: OAuth bearer token, obtained using client_id and client_secret.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    return bearer_token

def request(host, path, bearer_token, url_params=None):
    """Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()

def search(bearer_token, term, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)


def query_api(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)

    response = search(bearer_token, term, location)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return
    print "GOT Business "
    print businesses
    return businesses;





def yelp(req,term,loc):
    term = term
    location = loc
    print term
    print location
    businesses = query_api(term,location);

    return render(req,"yelp.html",{"businesses":businesses})

