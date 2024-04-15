from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.conf import settings
from django.core.mail import send_mail
from app.models import Books
from app.models import issue,bag,rented,category,userdata,lostdata,purchase
import datetime, string, random

# Create your views here.
def home(request):
    book =Books.objects.all()
    count=book.count()
    return render(request,"land.html",{'book':book,'count':count})

def sign(request):
    return render(request,'signup.html')

def genere(request):
    return render(request,'genere.html')

def AddGenere(request):
    if request.method == 'POST':
        genere=request.POST['genere']
        data = category(ctgname=genere)
        data.save()
        messages.info(request, 'Added')
        return redirect('genere')

def admin(request):
    active=User.objects.filter(is_superuser=0,is_active=1)
    books=Books.objects.count()
    count=active.count()
    rentb=rented.objects.count()
    inactive=User.objects.filter(is_active=0).count()
    due=rented.objects.filter(finestatus="Not Paid").count()
    context={'count':count,'books':books,'rent':rentb,'icount':inactive,'due':due}
    return render(request,"admin.html",context)

login_required
def user(request):
    books=Books.objects.all()
    return render(request,"user2.html",{'books':books})

def abooks(request):
    genere=category.objects.all()
    inactive=User.objects.filter(is_active=0).count()
    due=rented.objects.filter(finestatus="Not Paid").count()
    context={'icount':inactive,'due':due,'genere':genere}
    return render(request,"add.html",context)

def signup(request):
    if request.method == "POST":
        first_name = request.POST["fname"]
        last_name = request.POST['lname']
        username = request.POST['uname']
        email = request.POST["email"]
        place=request.POST["place"]
        phone=request.POST["phone"]
        image=request.FILES.get('file')
        if image==None:
            image='/static/men.png'
        else:
            image=request.FILES.get("file")
        if User.objects.filter(username=username).exists():
            messages.info(request, "This username is already taken")
            return redirect("home")
        elif User.objects.filter(email=email).exists():
            messages.info(request,"this mail id is already exist!")
            return redirect('home')
        else:
            def make_random_password(length=6):
                digits = string.digits
                all_chars =digits
                password = ''.join(random.sample(all_chars, length))
                return password
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
            )
            user.is_active=False
            user.save()
            password = make_random_password(length=6)

            user.set_password(password)
            user.save(update_fields=['password'])
            subject = 'Resgistration'
            message = 'Dear  '+str(user)+' your password'+'\n'+password
            recipient = email     #  recipient =request.POST["inputTagName"]
            send_mail(subject, 
            message, settings.EMAIL_HOST_USER, [recipient])
            userd=User.objects.get(id=user.id)
            data=userdata(address=place,phone=phone,image=image,user=userd)
            data.save()
            return redirect("home")
    else:
        return render(request, "test.html")

def log(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        uname=User.objects.get(username=username)
        if(uname.is_active==0):
            messages.info(request, "Approval Pending")
            return redirect("home")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # it means that there is a valid user, and the code block within the if block will be executed.
            auth.login(request,user)
            a=user.is_active
            print(a)
            username=User.objects.get(username=username)
            if(user.is_superuser):
                return redirect("admin")
            else:
                request.session['uid']=user.id
                return redirect("user")
        else:
            messages.info(request, "Invalid password or Password")
            return redirect("home")
    else:
        return redirect("home")

def addfun(request):
    if request.method == "POST":
        bname=request.POST["name"]
        author=request.POST["author"]
        select=request.POST['select']
        genere=category.objects.get(id=select)
        pid=request.POST["publisher"]
        quantity=request.POST["quantity"]
        price=request.POST["price"]
        rent=request.POST["rent"]
        summary=request.POST["summary"]
        image=request.FILES.get("file")
        book=Books(book_name=bname,
                   author_name=author,
                   genere=genere,
                   publisherid=pid,
                   quantity=quantity,
                   price=price,
                   rent=rent,
                   image=image,
                   summary=summary,
        )
        book.save()
        messages.info(request,"Book added Successfully")
        return redirect('abooks')

def showbooks(request):
    books=Books.objects.all()
    return render(request,"showbooks.html",{'books':books})

def userbooks(request):
    books=Books.objects.all()
    return render(request,"userbook.html",{'books':books})

def check(request):
    books=Books.objects.all()
    i=issue.objects.all()
    return render(request,"userbook.html",{'books':books},{'check':i})

def logout(request):
        auth.logout(request)
        return redirect('home')

def users(request):
    users=userdata.objects.all()
    return render(request,"users.html",{'users':users})

def newusers(request):
    users=User.objects.all()
    for p in users:
        if (p.is_active==0):
            flag=1
            break
        else:
            flag=0
            continue
    if flag==1:
        users=User.objects.filter(is_active=0)
        return render(request,"newuser.html",{'users':users})
    else:
        return render(request,"emptyuser.html")

def editbooks(request,bookId):
    print(bookId)
    book=Books.objects.get(id=bookId)
    genere=category.objects.all()
    context={'book':book,'generes':genere}
    return render(request,'editbooks.html',context)

def updatebooks(request,bookId):
    book= Books.objects.get(id=bookId)
    if request.method == 'POST':
        book.book_name=request.POST['name']     
        book.author_name=request.POST['author']
        book.genere.ctgname=request.POST['category'] 
        book.quantity=request.POST['quantity'] 
        book.price=request.POST['price'] 
        book.rent=request.POST['rent']
        image=request.FILES.get('file')
        if image is not None:
            book.image=image
        book.save()
        return redirect('showbooks')
    else:
        return redirect('editbooks')

def deletebooks(request,bookId):  
     book = Books.objects.get(id=bookId)
     book.delete()
     return redirect('showbooks')

def approve(request,userid):
     user=User.objects.get(id=userid)
     user.is_active=1
     user.save()
     messages.info(request, "one user Approved")
     return redirect('newusers')

def decline(request,userid):  
     user = User.objects.get(id=userid)
     user.delete()
     return redirect('newusers')

def remove(request,userid):  
     user = User.objects.get(id=userid)
     user.delete()
     return redirect('users')

def profile(request):
    if 'uid' in request.session:
        userId = request.session['uid']
        useid=User.objects.get(id=userId)
        print(useid.id)
        user = userdata.objects.get(user_id=useid)
        return render(request,'profile.html',{'user':user})
    else:
        return redirect('login_function')

def changepass(request):
    return render(request,"changepass.html")
    
def changepwd(request):
    if request.method=="POST":
        use = request.session['uid']
        useid=User.objects.get(id=use)
        username=useid.username
        oldpassword=request.POST["opassword"]
        opass=useid.password
        print(opass)
        user=auth.authenticate(username=username,password=oldpassword)
        newpassword=request.POST["npassword"]
        if user is not None:
            user=User.objects.get(username=username)
            user.set_password(newpassword)
            user.save(update_fields=['password'])
            return redirect("home")
        else:
            messages.info(request,"invalid password")
            return redirect("changepass")
    else:
        return redirect("user")
    
def editpage(request):
    userid= request.session['uid']
    user=userdata.objects.get(user_id=userid)
    return render(request,'edituser.html',{'user':user})

def updateuser(request,userid):
    if request.method == 'POST':
        user=User.objects.get(id=userid)
        username=request.POST["username"]
        if username==user.username:
            user.username=request.POST["username"]
        else:
            if User.objects.filter(username=username).exists():
                messages.info(request,"username already taken")
                return redirect('editpage')  
            else:
                 user.username=request.POST["username"]
        customer=userdata.objects.get(user_id=userid)
        user.first_name = request.POST["fname"]
        user.last_name = request.POST['lname']
        email = request.POST["email"]
        if email==user.email:
            user.email = request.POST["email"]
        else: 
            if User.objects.filter(email=email).exists():
                messages.info(request,"email already taken")
                return redirect("editpage")
            else:
                user.email = request.POST["email"]
        customer.address=request.POST["place"]
        customer.phone=request.POST["phone"]
        old=customer.image
        new=request.FILES.get('file')
        
        if old !=None and new==None:
            customer.image=old
        else:
            customer.image=new
        user.save()
        customer.save()
        return redirect('profile')
    
def checkout(request,bookId):
    book=Books.objects.get(id=bookId)
    q=book.quantity
    if q<1:
        messages.info(request, "Out of stock")
        return redirect('user')
    else:
       return render(request,'check.html',{'book':book})

# def addcart(request,bookId):
#     user= request.session['uid']
#     book=Books.objects.get(id=bookId)
#     q=book.quantity
#     if int(q)<1:
#         messages.info(request, "Out of stock")
#         return redirect('user')
#     cart=bag.objects.filter(user_id=user)
#     for p in cart:
#         if p.book_id==bookId:
#            p.quantity+=1
#            p.save()
#            book.quantity-=1
#            book.save()
#            return redirect('cartpage')
#     data=bag(user_id=user,book_id=bookId)
#     data.save()
#     book.quantity-=1
#     book.save()
#     return redirect('cartpage')
    
def addcart(request,bookId):
    user= request.session['uid']
    book=Books.objects.get(id=bookId)
    q=book.quantity
    if int(q)<1:
        messages.info(request, "Out of stock")
        return redirect('user')
    cart=bag.objects.filter(user_id=user)
    for p in cart:
        if p.quantity==q:
           messages.info(request, "you cannot add more than available stock")
           return redirect('cartpage')
        elif p.book_id==bookId:
             p.quantity+=1
             p.save()
             return redirect('cartpage')
    data=bag(user_id=user,book_id=bookId)
    data.save()
    return redirect('cartpage')

def cartpage(request):
    userid= request.session['uid']
    user=User.objects.get(id=userid)
    cart=bag.objects.filter(user=user)
    total_price=sum(item.total_price() for item in cart)
    context={'cart':cart,'total_price':total_price}
    if total_price==0:
        return render(request,'emptycart.html')
    else:
        return render(request,'cart.html',context)

def increase(request,cid):
    cart_item=bag.objects.get(id=cid)
    bid=cart_item.book_id
    book=Books.objects.get(id=bid)
    if book.quantity==0:
        messages.info(request, "Out of stock")
        return redirect('cartpage')
    elif cart_item.quantity == book.quantity:
        messages.info(request, "you cannot add more than available stock")
        return redirect('cartpage')
    else:
        cart_item.quantity+=1
        cart_item.save()
        return redirect('cartpage')


def decrease(request,cid):
    cart_item=bag.objects.get(id=cid)
    if cart_item.quantity==1:
        cart_item.delete()
        return redirect('cartpage')
    else:
        cart_item.quantity-=1
        cart_item.save()
        return redirect('cartpage')

def removecart(request,cartid):
    cart=bag.objects.get(id=cartid)
    cart.delete()
    return redirect(cartpage)

 
def place(request,bookId):
    if request.method=='POST':
        book=Books.objects.get(id=bookId)
        rent=int(book.rent)
        d1=request.POST['fdate']
        d2=request.POST['tdate']
        now=datetime.datetime.now().strftime ("%Y%m%d")
        date_format = "%Y-%m-%d"
        a = datetime.datetime.strptime(str(d1), date_format)
        b = datetime.datetime.strptime(str(d2), date_format)
        delta = b - a
        total=(int(delta.days))*rent
        print(delta)
        print(total)
        context={'book':book,'from':d1,'to':d2,'total':total,'days':delta.days}
        return render(request,'place.html',context)

def order(request,bookId):
        if request.method=='POST':
            user= request.session['uid']
            userid=User.objects.get(id=user)
            bookid=Books.objects.get(id=bookId)
            bookid.quantity=(bookid.quantity)-1
            bookid.save()
            d1=request.POST['fdate']
            d2=request.POST['todate']
            total=request.POST['total']
            date_format = "%Y-%m-%d"
            now=datetime.datetime.now().date()
            a = datetime.datetime.strptime(str(d2), date_format)
            b = datetime.datetime.strptime(str(now), date_format)
            # if b>a:
            #   delta=b-a
            #   fine=(int(delta.days))*30
            # else:
            fine=0
            if fine==0:
                status="N/A"
            else:
                status="NOT PAID"
            data=rented(fromdate=d1,todate=d2,total=total,
                        fine=fine,book=bookid,user=userid,finestatus=status,returns="Not Return")
            data.save()
            subject="order"
            message = 'Dear  '+str(userid.username)+'\n'+'your order for book '+'"'+bookid.book_name+'"'+' was suceessfully placed'
            recipient = userid.email     #  recipient =request.POST["inputTagName"]
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
            return redirect('issued')
 
def payment(request):
    return render(request,'payment.html')

# def issued(request):
#     user= request.session['uid']
#     userid=User.objects.get(id=user)
#     issue=rented.objects.filter(user=userid)
#     context={'issue':issue}
#     return render(request,'rented.html',context)

def issued(request):
    user= request.session['uid']
    userid=User.objects.get(id=user)
    issue=rented.objects.filter(user=userid)
    now=datetime.datetime.now().date()
    date_format = "%Y-%m-%d"
    for p in issue:
        d2=p.todate
        a = datetime.datetime.strptime(str(d2), date_format)
        b = datetime.datetime.strptime(str(now), date_format)
        if p.returns=="Not Return" and b>a:
            delta=b-a
            p.fine=(int(delta.days))*30
            p.finestatus="Not Paid"
            p.save()
        else:
            continue
    context={'issue':issue}
    return render(request,'rented.html',context)

def purchased(request):
    user= request.session['uid']
    userid=User.objects.get(id=user)
    buyed=purchase.objects.filter(user_id=user)
    context={'buy':buyed}
    return render(request,'purchased.html',context)

def losted(request):
    user= request.session['uid']
    userid=User.objects.get(id=user)
    lost=lostdata.objects.filter(user_id=userid)
    context={'lost':lost}
    return render(request,'lostbook.html',context)

def tissued(request):
    issue=rented.objects.all()
    context={'issue':issue}
    return render(request,'totalrented.html',context)

def tpurchased(request):
    buyed=purchase.objects.all()
    context={'buy':buyed}
    return render(request,'totalpurchased.html',context)

def tlosted(request):
    lost=lostdata.objects.all()
    context={'lost':lost}
    return render(request,'totalost.html',context)

  
def viewpage(request,bookId):
    book=Books.objects.get(id=bookId)
    context={'book':book}
    return render(request,'viewpage.html',context)
   
def bookpage(request,bookId):
    book=Books.objects.get(id=bookId)
    return render(request,'bookpage.html',{'book':book})

def search(request):
    if request.method=='POST':
        search_query = request.POST['search']
        search=search_query.upper()
        print(search)
        cat=category.objects.all()
        for p in cat:
          if(p.ctgname==search):
            print(p.ctgname)
            flag=1
            break
          else:
              flag=0
              continue
        if flag==1:
            generename=category.objects.get(ctgname=search)
            genereid=generename.id
            generenam=Books.objects.filter(genere=genereid)
            return render(request,'bookie.html',{'books':generenam})
        else:
            books = Books.objects.filter(book_name=search)
            books = Books.objects.filter(author_name=search)
            return render(request,'bookie.html',{'books':books})

def usearch(request):
    if request.method=='POST':
        search_query = request.POST['search']
        search=search_query.upper()
        print(search)
        cat=category.objects.all()
        for p in cat:
          if(p.ctgname==search):
            print(p.ctgname)
            flag=1
            break
          else:
              flag=0
              continue
        if flag==1:
            generename=category.objects.get(ctgname=search)
            genereid=generename.id
            generenam=Books.objects.filter(genere=genereid)
            return render(request,'usearch.html',{'books':generenam})
        else:
            books = Books.objects.filter(book_name=search)
            for p in books:
                if p.book_name==search:
                    flag=1
                    break
                else:
                    flag=0
                    continue
            if flag==1:
                return render(request,'usearch.html',{'books':books})
            else:
                books = Books.objects.filter(author_name=search)
                return render(request,'usearch.html',{'books':books})

def lost(request,rentid):
    rent=rented.objects.get(id=rentid)
    fine=rent.fine
    price=rent.book.price
    total=int(fine)+int(price)+35
    context={'rent':rent,'price':total}
    return render(request,'lost.html',context)

def lostbook(request,rentid):
    user= request.session['uid']
    rm=rented.objects.get(id=rentid)
    fine=rm.fine
    bid=rm.book_id
    book=Books.objects.get(id=bid)
    price=book.price
    now=datetime.datetime.now().date()
    total=int(fine)+int(price)+35
    data=lostdata(book_id=bid,user_id=user,price=total,fine=fine,date=now)
    data.save()
    rm.delete()
    return redirect('losted')

def purchas(request,bookid):
    bookid=Books.objects.get(id=bookid)
    return render(request,'purchase.html',{'book':bookid})

def cartpurchas(request,cartid):
    cart=bag.objects.get(id=cartid)
    bid=cart.book_id
    bookid=Books.objects.get(id=bid)
    if cart.quantity==0:
        messages.info(request, "Add atleast one quqntity")
        return redirect('cartpage')
    elif cart.quantity > bookid.quantity:
        messages.info(request,"Quantity greater than stock")
        return redirect('cartpage')
    if bookid.quantity == 0:
        messages.info(request, "out of stock")
        return redirect('cartpage')
    else:
        quantity=cart.quantity
        price=cart.total_price
        context={'book':bookid,'quantity':quantity,'price':price,'cart':cart}
        return render(request,'cartpurchase.html',context)

def buy(request,bookid):
    user= request.session['uid']
    bookie=Books.objects.get(id=bookid)
    if bookie.quantity == 0:
        messages.info(request, "you cannot add more than available stock")
        return redirect('cartpage')
    else:
        bookie.quantity=(bookie.quantity)-1
        bookie.save()
        now=datetime.datetime.now().date()
        data=purchase(user_id=user,book_id=bookid,date=now)
        data.save()
        return redirect('issued')

def cartbuy(request,cartid):
    user= request.session['uid']
    cart=bag.objects.get(id=cartid)
    bid=cart.book_id
    quantity=cart.quantity
    bookie=Books.objects.get(id=bid)
    bookie.quantity=(bookie.quantity)-quantity
    bookie.save()
    now=datetime.datetime.now().date()
    price=bookie.price*quantity
    print(price)
    data=purchase(user_id=user,book_id=bid,date=now,price=price,quantity=quantity)
    data.save()
    cart.delete()
    return redirect('purchased')

def payment(request,cartid):
    cart=bag.objects.get(id=cartid)
    return render(request,'buypay.html',{'cart':cart})

def rentpayment(request,rentid):
    rent=rented.objects.get(id=rentid)
    return render(request,'rentpay.html',{'rent':rent})

def dummy(request):
    return render(request,'dummy.html')

def finepay(request,rentid):
    rent=rented.objects.get(id=rentid)
    return render(request,'finepay.html',{'rent':rent})

def finestats(request,rentid):
    rent=rented.objects.get(id=rentid)
    rent.finestatus="PAID"
    rent.returns="Returned"
    rent.rdate=datetime.datetime.now().date()
    rent.save()
    return redirect('issued')

def returnpage(request,rentid):
    rent=rented.objects.get(id=rentid)
    if int(rent.fine)==0:
        return render(request,'returndue.html',{'rent':rent})
    else:
        return render(request,'return.html',{'rent':rent})

def returndue(request,rentid):
    rent=rented.objects.get(id=rentid)
    rent.finestatus="N/A"
    rent.returns="Returned"
    rent.rdate=datetime.datetime.now().date()
    rent.save()
    return redirect('issued')

def duemail(request,id):
    rent=rented.objects.get(id=id)
    user=rent.user.username
    due=rent.fine
    email=rent.user.email
    subject = 'Due Notification'
    message = 'Dear  '+str(user)+'\n'+'your have pending due of ₹'+due+'\n'+"please pay the due and return the book"
    recipient = email     #  recipient =request.POST["inputTagName"]
    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
    messages.info(request, "Mail Sent")
    return redirect('tissued')

