from django.db import models


Q_CHOICES = (
    (0,'Old'),
    (1,'Worn'),
    (2,'Good'),
    (3,'Like new'),
    (4,'New')
)

class book(models.Model):
	Title = models.CharField(max_length = 100) # Title of book.
	Author = models.CharField(max_length = 100)# Author of book.
	Publisher = models.CharField(max_length = 100)# Publisher of book.
	Genre = models.CharField(max_length = 100)# Genre of book.
	Abstract = models.TextField()# a short summary of book.
	Quality = models.IntegerField(choices = Q_CHOICES) #scale of book quality. 0 old, 1 like old, 2 good, 3 like new, 4 new
	Owner = models.ForeignKey('user')#the user that posted the book.
	Status = models.CharField(max_length = 10, default = 'nosale')
	NumofRates = models.IntegerField(default = 0) #to get and average rating.
	Rating = models.DecimalField(decimal_places=2, max_digits= 3, default = 0)
	FrontImage = models.ImageField('Book_Image', upload_to = 'image/', max_length = 500, default = '/image/book.jpg')
	BackImage = models.ImageField('Book_Image', upload_to = 'image/', max_length = 500, default = '/image/book.jpg')
	#Images will come from the book_image class; since each book can have many images.
	def dictof(self):
	    d = dict()
	    d['Title'] = self.Title
	    d['Author'] = self.Author
	    d['Publisher'] = self.Publisher
	    d['Genre'] = self.Genre
	    d['Abstract'] = self.Abstract
	    d['Quality'] = self.Quality
	    return(d)
	def __unicode__(self):
	    return(self.Title)

class user(models.Model): #user related fields 
	NumofRates = models.IntegerField(default = 0) #to get and average rating.
	Rating = models.DecimalField(decimal_places=2, max_digits= 3, default = 0)
	Type = models.CharField(max_length = 10) #types are SU, RU. not needed.
	UserName = models.CharField(max_length = 100)#user name.
	PassWord = models.CharField(max_length = 100)#Password
	FirstName = models.CharField(max_length = 100)# first name.
	LastName = models.CharField(max_length = 100)# last name.
	Email = models.EmailField(unique = True) # email address.
	Picture = models.ImageField('User_Pic', upload_to = 'image/', max_length = 500, null = True) #profile picture: just one pic.
	Verified = models.BooleanField(default = False) # This field will determine whether the user is Verified or not by an Admin.
	Wallet = models.IntegerField(default = 5) # the wallet stores all points a user has.
	def dictof(self):
	    d = dict()
	    d['UserName'] = self.UserName
	    d['PassWord'] = 'NotShared' # password is never shared.
	    d['FirstName'] = self.FirstName
	    d['LastName'] =  self.LastName
	    d['Email'] = self.Email
	    d['Picture'] = self.Picture
	    return(d)
	def __unicode__(self):
	    return(self.Email)
class visit_history(models.Model):
	VisitingUser = models.ForeignKey('user')
	DateTime = models.DateTimeField() #Date visited
class book_visit(models.Model):
	VisitingUser = models.ForeignKey('user')
	BookId = models.ForeignKey('book')
	DateTime = models.DateTimeField()
	def __unicode__(self):
	    return(str(self.VisitingUser)+ ',' + str(self.BookId))

class user_visit(visit_history):
	User = models.ForeignKey('user')
	def __unicode__(self):
	    return(str(self.VisitingUser)+','+str(self.User))
class complaints(models.Model): #master class of complaints
	DateTime = models.DateTimeField() #Date Posted.
	PostedBy = models.ForeignKey('user')# Id of the user posting th complaint.
	ComplaintText = models.TextField() # any message involved in complaint.

class user_complaints(complaints):
	User = models.ForeignKey('user')
	def __unicode__(self):
	    return(str(self.User))

class book_complaints(complaints):
	Book = models.ForeignKey('book')
	def __unicode__(self):
	    return(str(self.Book))

class comment(models.Model):
    PostDate = models.DateTimeField()
    PostedBy = models.ForeignKey('user')
    CommentText = models.TextField()
    def __unicode__(self):
	return(self.CommentText)
class book_comment(comment):
    Book = models.ForeignKey('book')
class user_comment(comment):
    User = models.ForeignKey('user')
class Trade(models.Model):
	PostDate = models.DateTimeField() # date and time of start bid.
	Book = models.ForeignKey('book')
	BuyOutPrice = models.IntegerField()#sale price for sales
	LastBidder = models.ForeignKey('user', null=True, blank=True, default = None) # Buyer for sales
	EndTime = models.DateTimeField()# set to the moment the book is baught. In Auctions, this is also the length of the Auction.
	Open = models.BooleanField()
	Payed = models.BooleanField(default = False)
	def __unicode__(self):
	    return(str(self.Book))
class sale(Trade):
    pass
class auction(Trade):
	BaseBidPrice = models.IntegerField()
	CurrentBidPrice = models.IntegerField()
	MinBidInc = models.IntegerField(default = 1)
class Bid(models.Model):# a small table to keep track of previous auctoins you have bidded in.
    Bidder = models.ForeignKey('user')
    Auction = models.ForeignKey('Trade')
    def __unicode__(self):
	return(str(self.Bidder) + ' '+ str(self.Auction))

class complaint_contest(models.Model):
    Complaint = models.ForeignKey('complaints')
    Explain = models.TextField()
    def __unicode__(self):
	return(str(self.PostDate))

class three_complaints(models.Model):
    User = models.ForeignKey('user')
    def __unicode__(self):
	return str(self.User)
#models.DecimalField(decimal_places=2, max_digits= 20) will leave this here just incase.