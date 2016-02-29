from django import forms
from datetime import *

class edit_user_form(forms.Form):
    UserName = forms.CharField(max_length = 100)#user name.
    FirstName = forms.CharField(max_length = 100)# first name.
    LastName = forms.CharField(max_length = 100)# last name.
    Image = forms.ImageField(required=False)

class change_password_form (forms.Form):
    CurrentPassWord = forms.CharField(label=
        'Current Password' ,max_length = 100,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    NewPassWord = forms.CharField(label='New Password', max_length = 100,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    RepeatPassWord = forms.CharField(label='Repeat Password', max_length = 100,widget=forms.PasswordInput(attrs={'class':'form-control'}))

class new_user_form(forms.Form):
    UserName = forms.CharField(max_length = 100)#user name.
    FirstName = forms.CharField(max_length = 100)# first name.
    LastName = forms.CharField(max_length = 100)# last name.
    Email = forms.EmailField() # email address.
    PassWord = forms.CharField(max_length = 100,widget=forms.PasswordInput )
    Image = forms.ImageField(required=False)


class login(forms.Form):
    Email = forms.EmailField()
    PassWord = forms.CharField(max_length = 100, widget=forms.PasswordInput )

Q_CHOICES = (
    (4,'New'),
    (3,'Like new'),
    (2,'Good'),
    (1,'Worn'),
    (0,'Old')
)

Date_Choices =(
    (1,'1 day 1 point'),
    (2,'1 week 5 points'),
    (3,'1 month 25 points')
)

Rating_Choices = (
    (1,'1 star'),
    (2,'2 stars'),
    (3,'3 stars'),
    (4,'4 stars'),
    (5,'5 stars')
)

Points_Choices = (
    (20, '15 points $20'),
    (40, '35 points $40'),
    (60, '55 points $60'),
    (80, '75 points $80'),
    (100, '95 points $100')
)

class new_book_form(forms.Form):
    Title = forms.CharField(max_length = 100, widget=forms.TextInput(attrs={'class':'form-control'}))
    Author = forms.CharField(max_length = 100, widget=forms.TextInput(attrs={'class':'form-control'}))
    Publisher = forms.CharField(max_length = 100, widget=forms.TextInput(attrs={'class':'form-control'}))
    Genre = forms.CharField(max_length = 100, widget=forms.TextInput(attrs={'class':'form-control'}))
    Abstract = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    Quality = forms.IntegerField(widget = forms.Select(choices = Q_CHOICES, attrs={'class':'form-control'}))
    FrontImage = forms.ImageField(required=False)
    BackImage = forms.ImageField(required=False)

class auction_form(forms.Form):
    BuyOutPrice = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    BaseBidPrice = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    MinBidInc = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    EndTime = forms.IntegerField(widget = forms.RadioSelect(choices = Date_Choices))

class sale_form(forms.Form):
    SalePrice = forms.IntegerField(label="Sale Price", widget=forms.TextInput(attrs={'class':'form-control'}))

class bid_form(forms.Form):
    Bid = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))

class rate_form(forms.Form):
    rating = forms.IntegerField(widget = forms.Select(choices = Rating_Choices, attrs={'class':'form-control'}))

class text_form(forms.Form): # text form for Comments and complaints.
    Text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))

class points_form(forms.Form):
    Amount = forms.IntegerField(widget = forms.Select(choices = Points_Choices, attrs={'class':'form-control'}))
    CardNumber = forms.IntegerField(required = False, widget=forms.TextInput(attrs={'class':'form-control'}))
    SecurityCode = forms.CharField(required = False, widget=forms.TextInput(attrs={'class':'form-control'}))
    Address = forms.CharField(widget = forms.Textarea(attrs={'class':'form-control'}), required = False)
