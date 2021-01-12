
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

        if request.session.get('uid') is not None:
            return redirect("/home",)
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
        request.session['email']=user['email']
        print(auth_fb.get_account_info(user['idToken']))
        return redirect("/home",)

def home(request):
    msg = request.GET.get('msg')
    if request.method == "GET":
        print(request.session.get('uid'))
        if request.session.get('uid') is not None and request.COOKIES['sessionid'] is not None:
            name=request.session.get('name')
            return render(request, "dashboard/dashboard.html",{'name':name})
        else:
            print("got to else")
            print(msg)
            return render(request, "register/login.html",{'msg':msg})



def user_logout(request):
   try:
       del request.COOKIES['sessionid']

       del request.session['uid']
       auth.current_user = None
       request.session.clear()
       return redirect("/")
   except KeyError:
    pass



