from django.shortcuts import render,redirect
from ChatRoom.forms import *
from ChatRoom.models import *
from django.contrib.auth import login, authenticate,logout
import time
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/')

# Create your views here.
def welcome(request):
    return render(request,"welcome.html",{})

def sign(request):
    error = []
    login_error=[]
    registerform = RegisterForm()
    context={"error":error,
         "login_error":login_error,
         "registerform":registerform}
    if request.method == "GET":
        return render(request,"sign.html",context)
    if request.method == "POST":
        print "post"
        ########################### sign up for new user ###########################
        if "signup_form" in request.POST:
            print "sign up"
            username=''
            emailaddress=''
            password=''
            confirmpassword=''
            registerform = RegisterForm(request.POST)
            if registerform.is_valid():
                username = registerform.cleaned_data["username"]
                emailaddress = registerform.cleaned_data["emailaddress"]
                password = registerform.cleaned_data["password"]
                confirmpassword = registerform.cleaned_data["confirmpassword"]
            else:
                print "blank error"
                error.append("Please fill in all the blanks.")
                return render(request,"sign.html",context)

            if password != confirmpassword:
                print "password matching error"
                error.append("The two password is not matching")
                return render(request,"sign.html",context)

            if len(User.objects.filter(email = emailaddress)) > 0:
                error.append('Email Address is already taken.')
                return render(request,"sign.html",context)

            if len(User.objects.filter(username = username)) > 0:
                error.append('Username is already taken.')
                return render(request,"sign.html",context)

            #pass all the error check now the new user could be registered
            new_user = User.objects.create_user(username=username, \
                                                password=password,\
                                                email=emailaddress)
            new_user.is_active = False;
            new_user.save()
            new_user = authenticate(username=username, \
                                     password=password)
            login(request, new_user)
            return redirect("/chatroom")

        ########################### login for old user ###########################
        if "login_form" in request.POST:
            print "login"
            username = request.POST['login_username']
            password = request.POST['login_password']
            # authenticate is to using username and password to judge whether the user exist
            user = authenticate(username=username, password=password)
            if user is not None :
                print("login in successfully")
                login(request, user)
                return redirect('/chatroom')
            else:
                login_error.append("Account doesn't exist or wrong password!")
                return render(request, 'sign.html', context)
    return render(request,"sign.html",{"registerform":registerform})

def chatroom(request):
    login_user = request.user
    error=[]
    chats=Chat.objects.all()
    if chats:
        maxid = Chat.objects.all().order_by("-id")[0].id
    else:
        maxid = 0
    context={ "login_user" : login_user,
              "error":error,
              "chats":chats,
              "last_updated":maxid}
    if request.method == "GET":
        return render(request,"chatroom.html",context)
    if request.method == "POST":
        print request.POST
        ########################### POST new chat ###########################
        if "content" in request.POST:
            content = request.POST["content"]
            if content:
                post_date = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
                new_chat = Chat.objects.create(author=login_user, \
                                                  content=content,\
                                                  post_date=post_date)
                new_chat.save()
                maxid = Chat.objects.all().order_by("-id")[0].id
                return redirect("/chatroom")
            else:
                error.append("You cannot post blank title or content")
                return render(request,"chatroom.html",context)

def ajax_refresh(request,last_updated):
    login_user = request.user
    chats = Chat.objects.all()
    newchats = []
    for chat in chats:
        if chat.id > int(last_updated):
            newchats.append(chat)
    print newchats
    if newchats:
        context={"newchats":newchats}
        return render(request,"ajax_refresh_chat.html",context)
    else:
        return render(request,"empty.html",{})

def max_chat_id(request):
    chats = Chat.objects.all()
    if chats:
        maxid = chats.order_by("-id")[0].id
    else:
        maxid = 0
    return render(request,"maxid.html",{"maxid":maxid})