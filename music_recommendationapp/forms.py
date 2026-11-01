from django import forms
from .models import Customer, Contact, Album, Song, Category, FreeAlbum, FreeSong, Subscription, Subscribers,Keyword


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude=['status']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = "__all__"


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["album", "title", "singer", "file", "category", "director"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = "__all__"





class FreeAlbumForm(forms.ModelForm):
    class Meta:
        model = FreeAlbum
        fields = "__all__"


class FreeSongForm(forms.ModelForm):
    class Meta:
        model = FreeSong
        fields = ["album", "title", "singer", "file", "category", "director"]


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = "__all__"


class SubscribersForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ['holder_name', 'card_number', 'cvv_number', 'bank_name']
