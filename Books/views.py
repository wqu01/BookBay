# Create your views here

from forms import *
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from models import *
from datetime import *
import md5
from django.db.models import Q



def Logged(r):# given request r, if the browswer contains the logged cookie, then he is logged with user r.session['USER']
    try:
	return(user.objects.get(id = r.session['USER'].id))
    except Exception:
	return(False)

def bids(u):
    if(not u):
	return(False)
    return(u.bid_set.all())
def index(request):
    u = Logged(request)
    
    return render(request, 'index.html', {'user': u, 'bids': bids(u)})

def AddUser(request):
    u = Logged(request)
    if u:
	return HttpResponseRedirect('/books/')
    if request.method == 'POST': # If the form has been submitted...
	form = new_user_form(request.POST, request.FILES)
	if form.is_valid(): # All validation rules pass
	    f = form.cleaned_data
	    m = md5.new()
	    m.update(f['PassWord'])
	    Pass = m.hexdigest()
	    try:
		im = request.FILES['Image']
	    except Exception:
		im = "image/cz.jpeg"
	    u = user(Verified = False, Type = 'RU', UserName = f['UserName'], FirstName = f['FirstName'], LastName = f['LastName'], Email = f['Email'], Picture = im, PassWord = Pass )
	    u.save()
	    return HttpResponseRedirect('/books/'+str(u.id)+'/')
    else:
	form = new_user_form()
    return render(request, 'newuser.html',{'form' : form, 'new' : True, 'user':u, 'bids': bids(u) })


def ViewUser(request,user_id):
    lu = Logged(request)
    same = False
    u = user.objects.get(pk=user_id)
    if(u):
	if(lu):
	    if(int(lu.id) == int(user_id)):
		same = True # same means that the user is in his own page
	    else:
		user_visit(VisitingUser = lu, DateTime = datetime.now(), User = u).save()
    return render(request, 'viewuser.html', {'user': lu, 'books':u.book_set.all(), 'same':same, 'OU': u, 'bids': bids(u), 'textform':text_form(), 'comments':u.user_comment_set.all()})


def ViewBook(request,book_id):
    u = Logged(request)
    b = book.objects.get(pk=book_id)
    if(u):
	if(b not in u.book_set.all()):
	    book_visit(VisitingUser = u, DateTime = datetime.now(), BookId = b).save()
    return render(request, 'viewbooks.html', {'book':b, 'user':u, 'bids': bids(u), 'textform':text_form(), 'comments':b.book_comment_set.all(), 'rate':rate_form })

def NotVerified(request):
    try:
	del( request.session['USER'])
	return render(request,'verify.html', {'user': False})
    except Exception:
	return(HttpResponseRedirect('/books/login/'))

def LogOut(request):
    try:
	del( request.session['USER'])
	return render(request,'logout.html', {'user': False})
    except Exception:
	return(HttpResponseRedirect('/books/login/'))

def LogIn(request):
    attempt = False
    u = Logged(request)
    if u :
        return HttpResponseRedirect('/books/'+str(u.id)+'/')

    if request.method == 'POST':
	form = login(request.POST)
	if form.is_valid():
	    f = form.cleaned_data
	    try:
		u = user.objects.get(Email = f['Email'])
		m = md5.new()
		m.update (str(f['PassWord']))
		if(str(u.PassWord) == str(m.hexdigest())):
		    request.session['USER'] = u
		    return HttpResponseRedirect('/books/'+str(u.id)+'/')
		else:
		    raise Exception
	    except Exception as bob: #if user does not exist.
		attempt = True
    else:
	form = login()
    return render(request, 'login.html', {'form' : form, 'attempt' : attempt, 'user':u,'bids': bids(u) })

def EditBook(request,bookid):
    u = Logged(request)
    if not u:
	return HttpResponseRedirect('/books/login/')
    b = book.objects.get(pk=bookid)
    if(b not in u.book_set.all()): # if the book does not belong to the logged user
	return('/books/'+ str(u.id)+'/')
    if request.method == 'POST':
	form = new_book_form(request.POST)
	if form.is_valid():
	    f = form.cleaned_data
	    b.Title = f['Title']
	    b.Author = f['Author']
	    b.Publisher = f['Publisher']
	    b.Genre = f['Genre']
	    b.Abstract = f['Abstract']
	    b.Quality = f['Quality']
	    b.save()
	    print "saved edits"
	    return(HttpResponseRedirect('/books/viewbook/'+str(b.id)+'/'))
    else:
	form = new_book_form(b.dictof())
    return render(request,'addbook.html', {'form' : form, 'new' : False, 'id' : b.id, 'user':u,'bids': bids(u) },)

def EditUser(request):
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login/')

    if request.method == 'POST':
	form = edit_user_form(request.POST, request.FILES)
	if form.is_valid():
	    f = form.cleaned_data
	    u.UserName = f['UserName']
	    u.FirstName = f['FirstName']
	    u.LastName = f['LastName']
	    try:
		u.Picture = request.FILES['Image']
	    except Exception: # no image was passed.
		pass # do nothing.
	    u.save()
	    return(HttpResponseRedirect('/books/'+str(u.id)+'/'))
    else:
	form = edit_user_form (u.dictof())
    return render(request, 'newuser.html', {'form' :form, 'new' : False, 'id' : u.id, 'user': u,'bids': bids(u) },)

def ChangePassWord(request):
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login/')
    
    attempt = False #second attempt?
    if request.method == 'POST':
	form = change_password_form(request.POST)
	if form.is_valid():
	    f = form.cleaned_data
	    try:
		if(f['NewPassWord'] != f['RepeatPassWord']):
		    raise Exception
		m = md5.new()
		m.update (str(f['CurrentPassWord']))
		if(str(u.PassWord) == str(m.hexdigest())):
		    m2 = md5.new()
		    m2.update(str(f['NewPassWord']))
		    u.PassWord = m2.hexdigest()
		    u.save()
		    return HttpResponseRedirect('/books/edituser/')
		else:
		    raise Exception
	    except Exception as bob: #if user does not exist.
		attempt = True

    else:
	form = change_password_form()
    return render(request,'password.html',{'form':form,'user':u, 'bids':bids(u), 'attempt' :attempt})
def RemoveBook(request, bookid): 
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login')
    try:
	b = book.objects.get(pk = bookid, Owner = u).delete()
	return HttpResponseRedirect('/books/' + str(u.id) +'/')
    except Exception:
	return HttpResponse( 'An unhandled error occured. We apologize dearly.')

def SaleSetup(request, bookid): # setup to put a book on sale.
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login')

    try:
	b = book.objects.get(pk = bookid)
	if(b not in u.book_set.all()):
	    raise ZeroDivisionError #using ZeroDivision to have a specific type of error to capture to know that something went wrong
	sale.objects.get(Book = b) #if this raises TypeError, then we continue.
	raise ZeroDivisionError
    except ZeroDivisionError: # if I catch ZeroDivisionError, then book is not users or book is already on sale or auction.
	return HttpResponseRedirect('/books/'+str(u.id)+'/')
    except Exception:# if we capture TypeError, then the book has no sale or auciton, and we continue.
	pass

    if request.method == 'POST':
	form = sale_form(request.POST)
	if form.is_valid():
	    f = form.cleaned_data
	    s = sale(PostDate = datetime.now(), Book = book.objects.get(pk = bookid), BuyOutPrice = f['SalePrice'], EndTime = datetime.now())#end time in sale is not so important.
	    s.save()
	    b.Status = 'sale'
	    b.save()
	    return HttpResponseRedirect('/books/sale/' + str(s.id) +'/')
    else:
	form = sale_form()
    return render(request, 'sale.html', {'form': form, 'user':u, 'id':bookid, 'bids': bids(u)})

def AuctionSetup(request,bookid): # setup to auction a book.
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login/')
    
    try:
	b = book.objects.get(pk = bookid)
	if(b not in u.book_set.all()):
	    raise ZeroDivisionError #using ZeroDivision to have a specific type of error to capture to know that something went wrong
	Trade.objects.get(Book = b) #if this raises TypeError, then we continue.
	raise ZeroDivisionError
    except ZeroDivisionError: # if I catch ZeroDivisionError, then book is not users or book is already on sale or auction.
	return HttpResponseRedirect('/books/'+str(u.id)+'/')
    except Exception:# if we capture TypeError, then the book has no sale or auciton, and we continue.
	pass

    if request.method == 'POST':
	form = auction_form(request.POST)
	if form.is_valid():
	    f = form.cleaned_data
	    Time = f['EndTime']
	    if Time == 1:
		if(u.Wallet < 1): #does he have enough coins?
		    return HttpResponseRedirect('/books/getpoints/')
		u.Wallet -=1
		t = datetime.now() + timedelta(1)
	    elif Time == 2:
		if(u.Wallet < 5):
		    return HttpResponseRedirect('/books/getpoints')
		t = datetime.now() + timedelta(7)
		u.Wallet -=5
	    else:
		if(u.Wallet < 25):
		    return HttpResponseRedirect('books/getspoints')
		t = datetime.now() + timedelta(30)
		u.Wallet -=25
	    u.save()
	    a = auction(PostDate = datetime.now(), EndTime = t, Book = b, BaseBidPrice = f['BaseBidPrice'], BuyOutPrice = f['BuyOutPrice'], CurrentBidPrice = 0, LastBidder = None, MinBidInc = f['MinBidInc'], Open = True)
	    a.save()
	    b.Status = 'auction'
	    b.save()
	    return HttpResponseRedirect('/books/auction/' + str(a.id) +'/')
    else:
	form = auction_form()
    return render(request, 'auction.html', {'form': form, 'id' : bookid, 'user':u, 'bids': bids(u)})

def AuctionBook(request,bookid): # view an auction by bookid
    b = book.objects.get(pk = bookid)
    au = auction.objects.get(Book = b)
    return HttpResponseRedirect('/books/auction/'+str(au.id)+'/')

def SaleBook(request,bookid): # view an auction by bookid
    b = book.objects.get(pk = bookid)
    s = sale.objects.get(Book = b)
    return HttpResponseRedirect('/books/sale/'+str(s.id)+'/')

def Auction(request,auctionid): # view an auction
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login')

    S = False #incse we are looking at Auction as sale.
    ## check if auction is still open.
    try:
        au = auction.objects.get(pk = auctionid)
    except Exception:
	try:
	    au = sale.objects.get(pk = auctionid)
	    S = True
	except Exception:
	    return HttpResponse('Error')
    b = au.Book

    if(not au.Open): # If the auction is over and you are the winner, take you to pay page.
	if(u != au.LastBidder and u != au.Book.Owner):
	    return HttpResponseRedirect ('/books/')


    bid2small = False #this will be passed to html file to check if the bid lower than the permitted bid.
    try:
	NB = au.CurrentBidPrice + au.MinBidInc
    except Exception:#we are dealing with a sale not an auction
	return render(request, 'viewauction.html', {'user':u, 'bids': bids(u), 'rate' : rate_form, 'Sale' : True, 'auction' : au })
    
    if au.CurrentBidPrice == -1:
	Sale = True
    else:
	Sale = False
    if request.method == 'POST':
	form = bid_form(request.POST)
	if form.is_valid():
	    f = form.cleaned_data
	    newbid = f['Bid']
	    if newbid < NB: # if the input is less than the current bid plus min incrememnt.
		bid2small = True# the input was smaller than allowed.
	    else:
		#first I check if my Wallet has enough to make the bid. if not then I will direct to buy points page.
		if(u.Wallet < newbid):
		    return HttpResponseRedirect('/books/getpoints/')
		#if I have more in wallet than bid is worth, then we move on.

		if(au.LastBidder != None):# if no bidders yet, we will not need to return funds to anyone.
		    au.LastBidder.Wallet += au.CurrentBidPrice # otherwise, we return the funds of the last bid to last bidder
		    au.LastBidder.save()
		u.Wallet -= newbid
		u.save()
		au.CurrentBidPrice = newbid
		au.LastBidder = u
		au.save()
		try: # tracking the bids that users have participated in. so that they may check the status.
		    Bid.objects.get(Auction= au, Bidder = u)
		except Exception: # bid object does not exists
		    Bid(Auction = au, Bidder = u).save()
		    #Bid objects allow us to track all Open Auctions and see who has bidded in them.
    else:
	form = bid_form()
    return render(request, 'viewauction.html', {'book':b, 'auction' : au, 'user' : u, 'form' : form, 'LTmin' :bid2small, 'NB':NB, 'bids': bids(u), 'rate' : rate_form(), 'Sale':Sale }) #NB is next bid price allowed

def Sale(request, saleid):
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login')
    S = sale.objects.get(pk = saleid)
    return render(request, 'viewsale.html', {'sale':S, 'user':u, 'bids': bids(u)})

def EndSale(request, saleid):
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login')
    S = Trade.objects.get(pk = saleid)
    S.Open = False
    S.LastBidder = u
    b = book.objects.get(id = S.Book.id)
    b.Status = 'sold'
    b.save()
    S.save()
    if(Bid.objects.filter(Bidder = u, Auction = S).count() == 0):
	Bid(Bidder = u, Auction = S ).save()
    try:
	au = auction.objects.get(id = saleid)
	au.LastBidder.Wallet += au.CurrentBidPrice
	au.LastBidder.save()
	au.CurrentBidPrice = -1
	au.save()
    except Exception as d:
	pass
    return HttpResponseRedirect('/books/auction/' +str(saleid) + '/' )
    

def DelSale(request,saleid):
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login')
    
    s = sale.objects.get(pk = saleid)
    s.Book.Status = 'nosale'
    s.Book.save()
    s.delete()
    return HttpResponseRedirect('/books/' + str(u.id) +'/')

def DelAuction(request,auctionid):
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login')

    au = auction.objects.get(pk = auctionid)
    #delete all Bid objects.
    try:
	Bid.objects.get(Auction = au).delete()
    #return the LastBidders points
	au.LastBidder.Wallet += au.CurrentBidPrice
	au.LastBidder.save()
    except Exception: #if no bidder yet.
	pass
    #change Book status to 'nosale'
    au.Book.Status = 'nosale'
    au.Book.save()
    #delete auction object.
    auction.objects.get(pk = auctionid).delete()
    return HttpResponseRedirect('/books/' + str(u.id) +'/')

##############################Rating#################################
########################################################################

def RateUser(request,userid):
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login')
    
    if request.method == 'POST':
	form = rate_form(request.POST)
	if form.is_valid():
	    f = form.cleaned_data
	    newrate = f['rating']
	    ruser = user.objects.get(pk = userid)
	    avg = ruser.Rating
	    cnt = ruser.NumofRates
	    sum_ = avg*cnt
	    newcount = cnt + 1
	    newavg =float ((sum_ + newrate)/newcount)
	    ruser.NumofRates = newcount
	    ruser.Rating = newavg
	    ruser.save()
    return render(request,'thankyou.html',{'user' :u,'bids' :bids(u)})

def RateBook(request,bookid):
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login')

    if request.method == 'POST':
	form = rate_form(request.POST)
	if form.is_valid():
	    f = form.cleaned_data
	    newrate = f['rating']
	    b = book.objects.get(pk = bookid)
	    avg = b.Rating
	    cnt = b.NumofRates
	    sum_ = avg*cnt
	    newcount = cnt + 1
	    newavg =float ((sum_ + newrate)/newcount)
	    b.NumofRates = newcount
	    b.Rating = newavg
	    b.save()
	    return HttpResponseRedirect('/books/viewbook/' + str(b.id)+ '/')

#########################################################################
###########################function to pay points########################
#########################################################################
def PaySale(request,_type,_id):
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login')

    au = Trade.objects.get(pk = _id)
    if(int(_type) == 0): # transaction type is auction
	#pay seller
	au = auction.objects.get(pk = _id)
	au.Book.Owner.Wallet += au.CurrentBidPrice
	au.Book.Owner.save()# book seller was paid.
	# remove Bid object
	Bid.objects.filter(Auction = au).delete()
	au.Payed = True #auction will now appear as paid.
	au.save()
	au.Book.Status = 'sold'
	au.Book.save()
	##auction will contine to stay open, just incase any complaints should be made.
    else: # transaction type is sale
	S = Trade.objects.get(pk = _id)
	# Buyer may not have enough Funds to pay. if so, will be sent to buy more points
	if u.Wallet < S.BuyOutPrice:
	    return HttpResponseRedirect('/books/getpoints/') ############################################BUYMOREPOINTS######################################
	S.Book.Owner.Wallet += S.BuyOutPrice
	S.Book.Owner.save()
	try:
	    Bid.objects.filter(Auction = au).delete() # just incase
	except Exception:
	    pass
	u.Wallet -= S.BuyOutPrice
	S.Open = False
	S.Payed = True
	S.LastBidder = u #this is so that if the logged user goes back to sale, or auction to add complaint, he is allowed in.
	S.save()
	u.save()
	S.Book.Status = 'sold'
	S.Book.save()
    return render( request, 'viewauction.html', {'user':u ,'bids': bids(u), 'rate' : rate_form(), 'dorate' : True, 'auction' : au })
###########################################################################
###########################################################################
## complaints will be created after a sale. If there was something wrong with either pay or book, then we give option of adding a complaint

def CreateComplaint(request):
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login')
    #in this page, we will have a

def AddBook(request):
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login/')

    if request.method == 'POST':
	form = new_book_form(request.POST, request.FILES)
	if form.is_valid():
	    f = form.cleaned_data
	    b = book(Title = f['Title'], Author = f['Author'], Publisher = f['Publisher'], Genre = f['Genre'], Abstract = f['Abstract'], Quality = f['Quality'], Owner = u, FrontImage = f['FrontImage'])
	    if(f['BackImage'] != None):
		 b.BackImage = f['BackImage']
	    b.save()
	    return HttpResponseRedirect('/books/'+str(u.id)+'/')
    else:
	form = new_book_form()
    return render( request, 'addbook.html', {'form' :form, 'new':True, 'user':u,'bids': bids(u) })

def BookComment(request,bookid):
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login/')
    
    b = book.objects.get(pk = bookid)

    if request.method == 'POST':
	form = text_form(request.POST)
	if form.is_valid():
	    f = form.cleaned_data
	    book_comment(Book = b, CommentText= f['Text'], PostDate = datetime.now(), PostedBy = u).save()
    return HttpResponseRedirect('/books/viewbook/' + str(b.id) + '/#com')

def UserComment(request,userid):
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login/')

    UseR = user.objects.get(pk = userid) #UseR is used to not conflict with other names that look the same.

    if request.method == 'POST':
	form = text_form(request.POST)
	if form.is_valid():
	    f = form.cleaned_data
	    user_comment(User = UseR, CommentText= f['Text'], PostDate = datetime.now(), PostedBy = u).save()
    return HttpResponseRedirect('/books/' + str(UseR.id) + '/#ucom')


def BookComplaint(request,bookid):
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login/')

    b = book.objects.get(pk = bookid)
    if request.method == 'POST': # If the form has been submitted...
	form = text_form(request.POST)
	if form.is_valid():
	    f = form.cleaned_data
	    book_complaints(DateTime = datetime.now(), PostedBy = u, ComplaintText = f['Text'], Book = b ).save()
	    if b.book_complaints_set.count() >= 3:
		user_complaints(DateTime = datetime.now(), PostedBy = u, ComplaintText = 'More than 3 complaints on same book', User= b.Owner).save()
		if b.Owner.user_complaints_set.count() >= 3:
		    three_complaints(User = b.Owner).save()

	    return HttpResponseRedirect('/books/viewbook/' + str(b.id) + '/' )
    else:
	form = text_form()
    return render(request, 'bookcomplaint.html', {'form' :form, 'user':u,'bids': bids(u), 'book': b })


def UserComplaints(request,userid):
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login/')

    faultuser= user.objects.get(pk = userid)
    if request.method == 'POST': # If the form has been submitted...
	form = text_form (request.POST)
	if form.is_valid():
	    f = form.cleaned_data
	    user_complaints(DateTime = datetime.now(), PostedBy = u, ComplaintText = f['Text'], User = faultuser).save()
	    if faultuser.user_complaints_set.count() >= 3:
		three_complaints(User = faultuser).save()
	    return HttpResponseRedirect('/books/' + str(faultuser.id) + '/' )
	    
    else:
	form = text_form()
    return render(request, 'usercomplaint.html', {'form' :form, 'user':u,'bids': bids(u), 'u' :faultuser }) # u is user at fault object.


def GetPoints(request):
    u = Logged(request)
    if not(u):
	return HttpResponseRedirect('/books/login/')
    
    if request.method == 'POST': # If the form has been submitted...
	form = points_form(request.POST)
	if form.is_valid():
	    f = form.cleaned_data
	    u.Wallet+= f['Amount']
	    u.save()
	    return render(request, 'thankyou.html', {'user':u, 'bids': bids(u)})
    else:
	form = points_form()
    return render(request, 'points.html',{'form' : form, 'user':u, 'bids': bids(u)})



#############################################################################################
######################### functions dedicated to brose and serach############################
#############################################################################################
def Browse(request):
    u = Logged(request)
    return render(request, 'browse.html', {'user':u, 'bids':bids(u), 'books':book.objects.all(), 'Users':user.objects.all(), 'auctions':auction.objects.all(), 'sales':sale.objects.all()})

def GetBooks(keywords):
    books = None
    for i in keywords.split(' '):
        query = book.objects.filter(Q(Title__contains = i) | Q(Author__contains = i) | Q(Publisher__contains = i)| Q(Genre__contains = i) | Q(Abstract__contains = i))
        if books == None:
            books = query
        else:
            books = books | query
    return(books)

def GetUsers(keywords):
    users = None
    for i in keywords.split(' '):
        query = user.objects.filter(Q(UserName__contains= i ) | Q(FirstName__contains= i ) | Q(LastName__contains= i) |Q(Email__contains= i))
        if users == None:
            users = query
        else:
            users = users | query
    return users

def GetAuctions(books, users):
    Auctions = None
    for i in books:
        query = auction.objects.filter(Book = i)
        if Auctions == None:
            Auctions = query
        else:
            Auctions = Auctions | query
    for i in users:
        query = auction.objects.filter(Book__Owner = i)
        if Auctions == None:
            Auctions = query
        else:
            Auctions = Auctions | query
        
    return Auctions


def GetSales(books, users):
    Sales = None
    for i in books:
        query = sale.objects.filter(Book = i)
        if Sales == None:
            Sales = query
        else:
            Sales = Sales | query
    for i in users:
        query = sale.objects.filter(Book__Owner = i)
        if Sales == None:
            Sales = query
        else:
            Sales = Sales | query
        
    return Sales


def Search(request):
    u = Logged(request)
    if request.method == 'POST': # If the form has been submitted...
	keyword = request.POST['keyword']
	users = GetUsers(keyword)
	books = GetBooks(keyword)
	auctions = GetAuctions(books,users)
	sales = GetSales(books, users)
    return render(request, 'browse.html', {'user':u, 'bids':bids(u), 'books': books, 'Users':users, 'auctions':auctions, 'sales':sales,'search' : True, 'keyword':keyword})
