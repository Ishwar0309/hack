from django.core.mail.backends import console
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
                dict1 = {'selfKey':key}
                #print(key)
                val = values
                val.update(dict)
                val.update(dict1)
                results.append(val)
    #print(results)
    print("results:", results)

    if request.method == 'POST':
        if "broadcast" in request.POST:
            temp = {
                'farmerId' : request.POST.get('farmerId'),
                'cropName' : request.POST.get('cropName'),
                'quantity' : int(request.POST.get('quantity')),
                'expectedPrice' : int(request.POST.get('expectedPrice')),
                'timestamp': datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
            }
            database.child("user").child("Farmer").child('yields').child(sess).push(temp)
        if "insurance" in request.POST:
                print("insure")

                temp ={
                    'processorKey': request.POST.get('processorKey'),
                    'farmerKey': request.POST.get('farmerKey'),
                    'interestKey':request.POST.get('selfKey'),

                }

                database.child("user").child("Quality Checker").child("0zGbx6o6oiWIqqABxfy5Qxo07kh2").child("check").push(temp)



    
    return render(request,'user/farmer.html',{'data':temp,'results':results})


def qualityChecker(request):
    result=[]
    resultData = database.child("user").child("Quality Checker").child("0zGbx6o6oiWIqqABxfy5Qxo07kh2").child("check").get()
    for check in resultData.each():
        value=check.val()
        
        
        
        user = database.child("user").child("Farmer").get()
      
        for i in user.each():
            dict1={}
            if(i.key()==value['farmerKey']):
                   

                userLotCheck = database.child("user").child("Processor").child("interests").child(value['processorKey']).get()  

                for j in userLotCheck.each():
                    #print(j.key())
                    #print(value['interestKey'])
                    dict2={}
                    if(j.key()==value['interestKey']):
                        
                        dict1=i.val()  
                        dict2=j.val()  
                        print("1:::::::",dict1) 
                        print("2:::::::",dict2) 
                        dict1.update(dict2)
                        print("com:::::::",dict1)
                        result.append(dict1)

    return render(request, 'user/qualityChecker.html',{'data':result})


def processor(request):
    data = database.child("user").child("Farmer").child('yields').get()
    temp = []
    processorId = request.session['uid']

    for entry in data.each():
        dict = {'farmerKey':entry.key()}

        hey = entry.val()
        for key,values in hey.items():
            val = values
            dict1={'farmerLotKey':key}
            val.update(dict)
            val.update(dict1)
            temp.append(val)
    if request.method == 'POST':
        print(request.POST)
        if "acceptButton" in request.POST:
            print('accept hua')
            data = {
                'farmerId': request.POST.get('farmerId'),
                'farmerLotKey' :request.POST.get('farmerLotKey'),
                'farmerKey': request.POST.get('farmerKey'),
                'cropName': request.POST.get('cropName'),
                'quantityRequested': request.POST.get('requiredQuantity'),
                'quotedPrice': request.POST.get('quotedPrice'),
                'quality': "N"
            }
            database.child("user").child("Processor").child('interests').child(processorId).push(data)

    # Broadcast for processor
    data = database.child("user").child("Processor").child("Confirmed Farmer Orders").child(processorId).get()
    lots =[]
    for lotKey in data.each():
        lots.append(lotKey.key())
    print(lots)
    if request.method == "POST":
        if "broadcast" in request.POST:
            product = {
                'lotKey': request.POST['dropdown'],
                'productName': request.POST.get('productName'),
                'quantity': int(request.POST.get('quantity')),
                'Price': int(request.POST.get('Price')),
                'timestamp': datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"),
                'availableQuantity' : int(request.POST.get('quantity'))
            }
            database.child("user").child("Processor").child('products').child(processorId).push(product)

    # display orders done with retailer
    temp=database.child("user").child("Retailer").child('Confirmed Processor Orders').get()
    RorderDetails=[]
    for ret in temp.each():
        y=ret.val()
        for key,z in y.items():
            if (z['processorKey']==request.session['uid']):
                RorderDetails.append(z)
    return render(request, 'user/processor.html',{'data':temp , 'lots' : lots,'orderDetails':RorderDetails} )

def retailer(request):
    data = database.child("user").child("Processor").child('products').get()
    productDetails = []
    retailerId = request.session['uid']
    for entry in data.each():
        processor = {'processorKey': entry.key()}
        product = entry.val()
        for key,value in product.items():
            dict = {"productKey" : key}
            details = value
            details.update(dict)
            details.update(processor)
            productDetails.append(details)
    print(productDetails)

    if request.method == "POST":
        if "accept" in request.POST:
            transaction = {
                # 'lotKey': request.POST.get('lotKey'),
                'productName': request.POST.get('productName'),
                'requiredQuantity': int(request.POST.get('requiredQuantity')),
                'Price': int(request.POST.get('Price')),
                'timestamp': datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"),
                'processorKey' : request.POST.get('processorKey'),
                'productKey': request.POST.get('productKey'),
                'reportAdded' : 0,
                'lotKey' : request.POST.get('lotKey')
            }
            processorKey = request.POST.get('processorKey')
            database.child("user").child("Retailer").child('Confirmed Processor Orders').child(retailerId).push(transaction)

            # change the available quantity
            
            requiredQuantity=int(transaction['requiredQuantity'])
            processorKey = transaction['processorKey']
            productKey = transaction['productKey']
            temp = database.child("user").child("Processor").child("products").child(processorKey).child(productKey).get()
            
            values=temp.val()
            avqty=int(values['availableQuantity'])
            avqty=avqty-requiredQuantity
            print(avqty)
                        
            database.child("user").child("Processor").child("products").child(processorKey).child(productKey).update({"availableQuantity": avqty})

    # display confirmed orders
    temp=database.child("user").child("Retailer").child('Confirmed Processor Orders').child(retailerId).get()
    orderDetails=[]
    for x in temp.each():
        z=x.val()
        
        orderDetails.append(z)


        
    return render(request , 'user/retailer.html' , {'data' : productDetails,'orderDetails':orderDetails})

def signIn(request):
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
    request.session['uid'] = str(session_id)
    #print(user)
    stake = request.POST['drop']

    

    users = database.child("user").child(stake).get()

    for u in users.each():
        if u.key() == session_id:
            context = u.val()
    if stake=="Farmer":
        return redirect("/farmer/")
    if stake=="Customer":
        return redirect("/customer/")
    if stake=="Logistics":
        return redirect("/logistics/")
    if stake=="Retailer":
        return redirect("/retailer/")
    if stake=="Processor":
        return redirect("/processor/")
    if stake=="Quality Checker":
        return redirect("/qualityChecker/")


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