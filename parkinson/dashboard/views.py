
from django.shortcuts import render, redirect
from firebase_repo import auth_fb,db
from django.contrib import auth
from django.contrib.auth import logout






# Create your views here.
from .forms import Login


def postsign(request):
    form = Login()
    email, password = None, None
    if request.method == "GET":
        if request.session.get('uid'):
            return redirect("/home")
        return render(request, "register/login.html", {"form": form})

    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
    try:
        user = auth_fb.sign_in_with_email_and_password(email,password)
    except:
        message = "invalid cerediantials"
        return render(request, "register/login.html",{'msg':message,'form':form})
    if (user):
        request.session['uid']=str(user['idToken'])
        current_doctor_id = db.child("Doctors").child(user['localId']).child("details").get()
        name=current_doctor_id.val()['first_name']+" "+current_doctor_id.val()['last_name']
        request.session['name'] = name
        # print(auth_fb.get_account_info(user['idToken']))
        return redirect("/home",)

#
# def home(response):
#     form = Login()
#     if response.method == "GET":
#         if response.user.is_active:
#             return redirect("/dashboard")
#         return render(response, "register/login.html", {"form": form})
#     else:
#         if response.method == "POST":
#             form = Login(response.POST)
#             if form.is_valid():
#                 username = form.cleaned_data['username']
#                 password = form.cleaned_data['password']
#                 user = authenticate(username=username, password=password)
#                 if user:
#                     if user.is_active:
#                         login(response, user)
#                         response.session['username'] = username
#                     return redirect("/dashboard")  # here  we  need to send the dictinoary and puplate it
#                 else:
#                     return render(response, "register/login.html",
#                                   {"form": form, 'error': "Username and Password did not match"})


def home(request):
    if request.method == "GET":
        name=request.session.get('name')
        return render(request, "dashboard/dashboard.html",{'name':name})


def user_logout(request):
   try:
       del request.session['uid']
       return redirect("/")
   except KeyError:
    pass



