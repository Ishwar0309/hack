from django.shortcuts import render
import pyrebase
from django.contrib import  auth as authe
from datetime import datetime
from django.shortcuts import redirect
# Create your views here.

firebaseConfig = {
    'apiKey': "AIzaSyB4bYmDeb3_B0juUAnSyviaRklqv6zKhFQ",
    'authDomain': "djangopyre-7902f.firebaseapp.com",
    'databaseURL': "https://djangopyre-7902f.firebaseio.com",
    'projectId': "djangopyre-7902f",
    'storageBucket': "",
    'messagingSenderId': "358747129386",
    'appId': "1:358747129386:web:642070b5130d61345fa553",
    'measurementId': "G-NHJFCCYS77"
  };


firebase =pyrebase.initialize_app(firebaseConfig)
database = firebase.database()
auth = firebase.auth()
def farmer(request):
    sess = request.session['uid']
    data = database.child("user").child("Farmer").child('yields').child(sess).get()
    temp = []
    if data.val() is not None:
        for i in data.each():
            temp.append(i.val())
    results = []
    resultData = database.child("user").child("Processor").child('interests').get()
    for entry in resultData.each():
        value = entry.val()
        for key,values in value.items():
            if values['farmerKey'] == sess:
                dict = {'processorKey':entry.key()}
                val = values
                val.update(dict)
                results.append(val)
    print(results)

    if request.method == 'POST':
        temp = {
        'farmerId' : request.POST.get('farmerId'),
        'cropName' : request.POST.get('cropName'),
        'quantity' : int(request.POST.get('quantity')),
        'expectedPrice' : int(request.POST.get('expectedPrice')),
        'timestamp': datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
        }
        database.child("user").child("Farmer").child('yields').child(sess).push(temp)
    return render(request,'user/farmer.html',{'data':temp,'results':results})

def processor(request):
    data = database.child("user").child("Farmer").child('yields').get()
    temp = []
    processorId = 'c1qWMfP0uZZt5vMNLHFOcLrzZwy1'
    for entry in data.each():
        dict = {'farmerKey':entry.key()}
        hey = entry.val()
        for key,values in hey.items():
            val = values
            val.update(dict)
            temp.append(val)
    if request.method=='POST':
        print(request.POST)
        if "acceptButton" in request.POST:
            print('accept hua')
            data = {
                'farmerId': request.POST.get('farmerId'),
                'farmerKey': request.POST.get('farmerKey'),
                'cropName': request.POST.get('cropName'),
                'quantityRequested': request.POST.get('requiredQuantity'),
                'quotedPrice': request.POST.get('quotedPrice')
            }
            database.child("user").child("Processor").child('interests').child(processorId).push(data)
    return render(request, 'user/processor.html',{'data':temp})
def singIn(request):
    # if method == 'POST':

    return render(request, 'user/signIn.html')


def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = auth.sign_in_with_email_and_password(email,passw)
    except:
        message ="Invalid credentials"
        return render(request,"user/signIn.html",{"msg":message})

    session_id = user['localId']
    request.session['uid']=str(session_id)
    print(user)
    stake = request.POST['drop']

    if stake=="Farmer":
        users = database.child("user").child(stake).get()

        for u in users.each():
            if u.key()==session_id:
                context= u.val()

                return redirect("/farmer/")

    if stake=="Farmer":
        users = database.child("user").child(stake).get()

        for u in users:
            if u.key()==session_id:
                context= u.val()

                return render(request,"user/farmer.html",context)

    if stake=="Farmer":
        users = database.child("user").child(stake).get()

        for u in users:
            if u.key()==session_id:
                context= u.val()

                return render(request,"user/farmer.html",context)

    users = database.child("user").child(stake).get()

    for u in users:
        if u.key() == session_id:
            context = u.val()
    if stake=="Farmer":
        return render(request,"user/farmer.html",context)
    if stake=="Customer":
        return render(request,"user/customer.html",context)
    if stake=="Logistics":
        return render(request,"user/logistic.html",context)
    if stake=="Retailer":
        return render(request,"user/retailer.html",context)
    if stake=="Processor":
        return render(request,"user/processor.html",context)
    if stake=="Quality Checker":
        return render(request,"user/qualityChecker.html",context)





def signUp(request):
    return render(request, 'user/signup.html')

def postsignUp(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    passw = request.POST.get('pass')
    stake = request.POST['drop']
    user = auth.create_user_with_email_and_password(email,passw)
    print(stake)
    print(email)
    id=user['localId']
    data={
        'name':name,
        'email':email,
    }

    database.child("user").child(stake).child(id).child('details').set(data)


    return render(request,"user/signIn.html")

def logout(request):

    authe.logout(request)
    return render(request, 'user/signIn.html')

def home(request):
    return render(request,'user/home.html')