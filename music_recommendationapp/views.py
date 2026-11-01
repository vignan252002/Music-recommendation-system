from django.shortcuts import render, redirect
from music_recommendationapp.models import FreeSong
from music_recommendationapp.forms import ContactForm
from .models import *

def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

def contact(request):
    msg = ""
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/contact?success=True")
    if request.GET.get('success'):
        msg = "Thank You For Contacting Us"
    return render(request, "contact.html", {"msg": msg, "form": form})


from django.db.models import Q
from .models import Keyword, Song, FreeSong




def play_song(request, id):
    song = FreeSong.objects.get(id=id)
    email = request.session.get('email')

    if email:
        CustomerListenHistory.objects.create(
            customer_email=email,
            song_id=song.id,
            album_id=song.album.id,
            song_title=song.title,
            singers=song.singer,         # NEW: Saving the singer
            category=song.category,      # NEW: Saving the category
            song_type="free"
        )

    return render(request, 'play_song.html', {'song': song})

#<------------------------------------Admin----------------------------------------------------->
#<------------------------------------Admin----------------------------------------------------->
#<------------------------------------Admin----------------------------------------------------->

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from music_recommendationapp.models import (
    Customer, Admin, Contact, Album, Song, Category,
    FreeAlbum, FreeSong, Subscription, Subscribers
)
from music_recommendationapp.forms import (
    AlbumForm, SongForm, CategoryForm, FreeAlbumForm,
    FreeSongForm, SubscriptionForm
)

# --- Authentication & Dashboard ---
def is_login(request):
    return request.session.__contains__("email")

def admin_login(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        login_check = Admin.objects.filter(email=email, password=password)
        if login_check.exists():
            request.session["email"] = email
            return render(request, "admin_home.html", {"msg": "Login Successful"})
        else:
            return render(request, "admin_login.html", {"msg": "Email And Password Does Not Match"})
    return render(request, "admin_login.html", {})

def admin_home(request):
    return render(request, "admin_home.html", {})

def admin_logout(request):
    return redirect('admin_login')

def admin_change_password(request):
    email = request.session.get("email")
    if is_login(request):
        if request.method == 'POST':
            password = request.POST['old_password']
            new_password = request.POST['new_password']
            if password == new_password:
                return render(request, "admin_change_password.html",
                              {"msg": "Your Old Password And New Password Are Same.", "email": email})
            try:
                user = Admin.objects.get(email=email, password=password)
                user.password = new_password
                user.save()
                messages.success(request, 'Password Changed Successfully')
                return redirect('/admin_login')
            except Exception as e:
                print(e)
                return render(request, "admin_change_password.html", {"msg": "Invalid Credentials", "email": email})
        return render(request, "admin_change_password.html", {"email": email})
    return redirect('/admin_login')

# --- User Management ---
def view_customer(request):
    con = Customer.objects.all()
    return render(request, "view_customers.html", {"con": con})

def admin_delete_customer(request, id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    return redirect("/view_customer")

def view_contact(request):
    con = Contact.objects.all()
    return render(request, "view_contacts.html", {"con": con})

def admin_view_subscribers(request):
    subscribers = Subscribers.objects.select_related('subscription').all()
    today = timezone.now().date()
    return render(request, "admin_view_subscribers.html", {"subscribers": subscribers, "today": today})

# --- Premium Albums & Songs ---
def add_album(request):
    email = request.session.get("email")
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                image = form.cleaned_data.get('image')
                if image and not image.content_type.startswith('image/'):
                    return render(request, "add_album.html", {"email": email, "msg": "Please upload a valid image file."})
                form.save()
                return redirect("/view_album")
            else:
                return render(request, "add_album.html", {"email": email, "msg": "Form is not valid."})
        except Exception as e:
            print(e)
            return render(request, "add_album.html", {"email": email, "msg": "Error during album creation."})
    return render(request, "add_album.html", {"email": email})

def view_album(request):
    album = Album.objects.all()
    return render(request, "view_album.html", {"album": album})

def edit_album(request, id):
    album = Album.objects.get(id=id)
    return render(request, "edit_album.html", {"x": album})

def update_album(request):
    if request.method == "POST":
        id = request.POST["id"]
        user = Album.objects.get(id=id)
        form = AlbumForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/view_album')
    return redirect('/view_album')

def delete_album(request, id):
    album = Album.objects.get(id=id)
    album.delete()
    return redirect('/view_album')

def add_song(request, id):
    email = request.session.get("email")
    album = Album.objects.get(id=id)
    category = Category.objects.all()
    if request.method == "POST":
        form = SongForm(request.POST, request.FILES)
        print(form.errors)
        try:
            if form.is_valid():
                form.save()
                return redirect("/view_song/{}".format(album.id))
        except Exception as e:
            print(e)
            return render(request, "add_song.html", {"category": category, "album": album, "msg": "Song Not Added"})
    return render(request, "add_song.html", {"category": category, "album": album,"Email":email})

def view_song(request, id):
    song = Song.objects.filter(album_id=id)
    return render(request, "view_song.html", {"song": song})

def edit_song(request, id):
    song = Song.objects.get(id=id)
    category = Category.objects.all()
    return render(request, "edit_song.html", {"x": song, "category": category})

def update_song(request):
    if request.method == "POST":
        id = request.POST["id"]
        user = Song.objects.get(id=id)
        form = SongForm(request.POST, request.FILES, instance=user)
        album_id = user.album_id
        if form.is_valid():
            form.save()
            return redirect('/view_song/{}'.format(album_id))
        return redirect('/view_song/{}'.format(album_id))

def delete_song(request, id):
    song = Song.objects.get(id=id)
    song.delete()
    return redirect('/view_song/{}'.format(song.album_id))

def admin_view_play_song(request, id):
    song = Song.objects.get(id=id)
    return render(request, 'admin_view_play_song.html', {'song': song})

# --- Free Albums & Songs ---
def add_free_album(request):
    email = request.session.get("email")
    if request.method == 'POST':
        form = FreeAlbumForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                form.save()
                return redirect("/view_free_album")
        except Exception as e:
            print(e)
            return render(request, "add_free_album.html", {"email": email, "msg": "Error"})
    return render(request, "add_free_album.html", {"email": email})

def view_free_album(request):
    album = FreeAlbum.objects.all()
    return render(request, "view_free_album.html", {"album": album})

def free_edit_album(request, id):
    album = FreeAlbum.objects.get(id=id)
    return render(request, "free_edit_album.html", {"x": album})

def free_update_album(request):
    if request.method == "POST":
        id = request.POST["id"]
        user = FreeAlbum.objects.get(id=id)
        form = FreeAlbumForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/view_free_album')
    return redirect('/view_free_album')

def free_delete_album(request, id):
    album = FreeAlbum.objects.get(id=id)
    album.delete()
    return redirect('/view_free_album')

def add_free_song(request, id):
    album = FreeAlbum.objects.get(id=id)
    category = Category.objects.all()
    if request.method == "POST":
        form = FreeSongForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                form.save()
                return redirect("/view_free_song/{}".format(album.id))
        except Exception as e:
            print(e)
            return render(request, "add_free_song.html", {"category": category, "album": album, "msg": "Song Not Added"})
    return render(request, "add_free_song.html", {"category": category, "album": album})

def view_free_song(request, id):
    song = FreeSong.objects.filter(album_id=id)
    return render(request, "view_free_song.html", {"song": song})

def free_edit_song(request, id):
    song = FreeSong.objects.get(id=id)
    category = Category.objects.all()
    return render(request, "free_edit_song.html", {"x": song, "category": category})

def free_update_song(request):
    if request.method == "POST":
        id = request.POST["id"]
        user = FreeSong.objects.get(id=id)
        form = FreeSongForm(request.POST, request.FILES, instance=user)
        album_id = user.album_id
        if form.is_valid():
            form.save()
            return redirect('/view_free_song/{}'.format(album_id))
        return redirect('/view_free_song/{}'.format(album_id))

def free_delete_song(request, id):
    song = FreeSong.objects.get(id=id)
    song.delete()
    return redirect('/view_free_song/{}'.format(song.album_id))

def admin_view_free_play_song(request, id):
    song = FreeSong.objects.get(id=id)
    return render(request, 'admin_view_free_play_song.html', {'song': song})

# --- Categories ---
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        category = request.POST.get("category")
        if Category.objects.filter(category=category).exists():
            return render(request, "add_category.html", {"msg": "This Category Already Exists !"})
        if form.is_valid():
            try:
                form.save()
                return redirect("/view_category")
            except Exception as e:
                print(e)
                return render(request, "add_category.html", {"msg": "Category Not Added"})
        else:
            return render(request, "add_category.html", {"msg": "Form is invalid", "form_errors": form.errors})
    return render(request, "add_category.html", {})

def view_category(request):
    category = Category.objects.all()
    return render(request, "view_category.html", {"cat": category})

def delete_category(request, id):
    cat = Category.objects.get(id=id)
    cat.delete()
    return redirect('/view_category')

# --- Subscription Plans ---
def add_plan(request):
    email = request.session.get('email')
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_plan')
        return render(request, "add_plan.html", {"email": email, "msg": "Plan Not Added, Please Try Again"})
    return render(request, "add_plan.html", {"email": email})

def view_plan(request):
    plan = Subscription.objects.all()
    return render(request, "view_plan.html", {"plan": plan})

def plan_delete(request, id):
    cus = Subscription.objects.get(id=id)
    cus.delete()
    return redirect('/view_plan')


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Customer  # Adjust import if necessary


def admin_update_customer_status(request, id, status):
    # Security check: ensure admin is logged in
    if 'email' not in request.session:
        return redirect('admin_login')

    customer = get_object_or_404(Customer, id=id)

    # Validate the status to prevent bad data injection
    valid_statuses = ['active', 'deactivated', 'pending', 'approved']

    if status in valid_statuses:
        customer.status = status
        customer.save()
        messages.success(request, f"Successfully updated status for {customer.fullname} to '{status.upper()}'.")
    else:
        messages.error(request, "Error: Invalid status requested.")

    return redirect('view_customer')

#<------------------------------------------------------------Customer------------------------------------------->
#<------------------------------------------------------------Customer------------------------------------------->
#<------------------------------------------------------------Customer------------------------------------------->
#<------------------------------------------------------------Customer------------------------------------------->

import random
import pandas as pd
from datetime import timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone

from music_recommendationapp.models import (
    Customer, Album, Song, FreeAlbum, FreeSong,
    Subscription, Subscribers, Keyword
)
from music_recommendationapp.forms import (
    CustomerForm, SubscribersForm, KeywordForm
)

# --- ML Recommendation Engine ---
# Load and vectorize CSV (Executed once when module loads)
df = pd.read_csv('tracks.csv')
df['combined'] = df['track_name'].astype(str) + ' ' + df['artist_name'].astype(str) + ' ' + df['album_name'].astype(str)
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['combined'])

def home(request):
    email = request.session.get('email')
    if not email:
        return render(request, 'home.html', {'results': [], 'query': ''})

    keywords = Keyword.objects.filter(email=email).values_list('keyword', flat=True)
    total_results = 10
    num_keywords = len(keywords)
    per_keyword = total_results // num_keywords if num_keywords > 0 else 0
    results = []

    for keyword in keywords:
        query_vec = vectorizer.transform([keyword])
        similarity = cosine_similarity(query_vec, tfidf_matrix)
        top_indices = similarity[0].argsort()[::-1][:per_keyword]

        keyword_results = df.iloc[top_indices][['track_name', 'artist_name', 'album_name', 'track_url', 'artwork_url']].to_dict(orient='records')
        results.extend(keyword_results)

    return render(request, 'home.html', {'results': results, 'query': ', '.join(keywords)})

# --- Authentication & Profile ---
def customer_is_login(request):
    return request.session.__contains__("email")

def customer_registration(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        email = request.POST.get('email')

        if Customer.objects.filter(email=email).exists():
            return render(request, "customer_registration.html",
                          {"msg": "This Email Already Exists. Can You Please Try With Another Email?"})
        else:
            if form.is_valid():
                try:
                    form.save()
                    subject = 'Registration Successful'
                    message = 'Welcome! Thank you for registering. Your account has been successfully created.'
                    from_email = 'your_email@gmail.com'
                    recipient_list = [email]
                    try:
                        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    except Exception as email_error:
                        print(f"User saved, but email failed to send: {email_error}")
                    return redirect('/customer_login')
                except Exception as e:
                    print(e)
                    return render(request, 'customer_registration.html', {"msg": "Registration Not Successful"})
    return render(request, "customer_registration.html", {})


import random
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import Customer  # Adjust based on your imports


def customer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # 1. Verify credentials
            customer = Customer.objects.get(email=email, password=password)
            if customer.status and customer.status.lower() == 'pending':
                messages.warning(request,
                                 "Your account is pending approval. Please wait for an administrator to activate your account.")
                return render(request, 'customer_login.html')

            elif customer.status and customer.status.lower() in ['rejected', 'deactivated', 'suspended']:
                messages.error(request, "Your account has been deactivated. Please contact support.")
                return render(request, 'customer_login.html')

            # 3. If status is approved/active, Generate the 6-digit OTP
            otp = str(random.randint(100000, 999999))

            # 4. Store email and OTP temporarily in session
            request.session['temp_email'] = email
            request.session['otp'] = otp

            # 5. Send OTP via email
            subject = 'Your Login OTP'
            message = f'Your One-Time Password for login is: {otp}'
            from_email = 'your_email@gmail.com'  # Ensure this matches your settings.py
            recipient_list = [email]

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                messages.success(request, f"An OTP has been sent to {email}")
                return redirect('verify_otp')  # Send user to the OTP entry page

            except Exception as e:
                print(f"Email failed: {e}")
                messages.error(request, "Failed to send OTP email. Please try again.")
                return render(request, 'customer_login.html')

        except Customer.DoesNotExist:
            messages.error(request, "Invalid Email or Password.")
            return render(request, 'customer_login.html')

    return render(request, 'customer_login.html')


from django.shortcuts import render, redirect
from django.contrib import messages


# You can remove the 'timezone' and 'Subscribers' imports from this file
# if they are no longer used anywhere else in this views.py file.

def verify_otp(request):
    # Security check: Ensure user came from the login page
    if 'temp_email' not in request.session:
        return redirect('customer_login')

    email = request.session['temp_email']

    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')

        if user_otp == session_otp:
            # OTP IS CORRECT: Complete the login process

            # 1. Set the actual logged-in session variable
            request.session['email'] = email

            # 2. Clean up temporary session data
            del request.session['temp_email']
            del request.session['otp']

            # 3. Redirect to customer home irrespective of subscription status
            return redirect('customer_home')

        else:
            # OTP IS INCORRECT
            messages.error(request, "Invalid OTP. Please try again.")

    # Render the OTP form if GET request or OTP was wrong
    return render(request, 'verify_otp.html', {'email': email})

def customer_home(request):
    return render(request, "customer_home.html", {})

def customer_logout(request):
    return redirect('customer_login')

def customer_change_password(request):
    email = request.session.get("email")
    if customer_is_login(request):
        if request.method == 'POST':
            password = request.POST['old_password']
            new_password = request.POST['new_password']
            if password == new_password:
                return render(request, "customer_change_password.html",
                              {"msg": "Your Old Password And New Password Are Same.", "email": email})
            try:
                user = Customer.objects.get(email=email, password=password)
                user.password = new_password
                user.save()
                messages.success(request, 'Password Changed Successfully')
                return redirect('/customer_login')
            except Exception as e:
                print(e)
                return render(request, "customer_change_password.html", {"msg": "Invalid Credentials", "email": email})
        return render(request, "customer_change_password.html", {"email": email})
    return redirect('/customer_login')

def customer_profile(request):
    email = request.session.get("email")
    customer = Customer.objects.get(email=email)
    return render(request, "customer_profile.html", {"customer": customer})

def customer_edit(request, id):
    customer = Customer.objects.get(id=id)
    return render(request, "customer_edit.html", {"x": customer})

def customer_update(request):
    if request.method == "POST":
        id = request.POST["id"]
        users = Customer.objects.get(id=id)
        users = CustomerForm(request.POST, instance=users)
        if users.is_valid():
            users.save()
        return redirect("/customer_profile")
    return redirect("/customer_profile")

# --- Content Viewing (Premium & Free) ---
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Album, Song, FreeAlbum, FreeSong, Subscribers  # Adjust imports as necessary


# --- Helper Function ---
def has_active_subscription(request):
    """Checks if the user in the current session has an active subscription."""
    email = request.session.get('email')
    if not email:
        return False

    active_subs = Subscribers.objects.filter(
        customer_email=email,
        enddate__gte=timezone.now().date()
    )
    return active_subs.exists()


# --- Premium Content (Restricted) ---

def customer_view_album(request):
    if not has_active_subscription(request):
        messages.warning(request,
                         "Premium Content: You are not subscribed. Please purchase a plan to access these albums.")
        return redirect('customer_view_plans')  # Redirects to your plans page

    album = Album.objects.all()
    return render(request, "customer_view_album.html", {"album": album})


def customer_view_song(request, id):
    if not has_active_subscription(request):
        messages.warning(request,
                         "Premium Content: You are not subscribed. Please purchase a plan to view these songs.")
        return redirect('customer_view_plans')

    email = request.session.get('email')
    song = Song.objects.filter(album_id=id)

    my_folders = []
    saved_song_ids = []  # <--- NEW: List to hold the IDs of songs they already saved

    if email:
        my_folders = UserPlaylist.objects.filter(customer_email=email)
        # Fetch IDs of all songs this user has saved in ANY folder
        saved_song_ids = Playlist.objects.filter(customer_email=email).values_list('song_id', flat=True)

    return render(request, "customer_view_song.html", {
        "song": song,
        "my_folders": my_folders,
        "saved_song_ids": list(saved_song_ids)  # <--- NEW: Pass it to the template
    })

from .models import CustomerListenHistory # Ensure this is imported at the top

def customer_view_song_play(request, id):
    if not has_active_subscription(request):
        messages.warning(request, "Premium Content: You are not subscribed. Please purchase a plan to play this song.")
        return redirect('customer_view_plans')

    song = Song.objects.get(id=id)
    email = request.session.get('email')

    if email:
        CustomerListenHistory.objects.create(
            customer_email=email,
            song_id=song.id,
            album_id=song.album.id,
            song_title=song.title,
            singers=song.singer,         # NEW: Saving the singer
            category=song.category,      # NEW: Saving the category
            song_type="premium"
        )

    return render(request, 'customer_view_song_play.html', {'song': song})


# --- Free Content (Unrestricted) ---

def customer_view_free_album(request):
    album = FreeAlbum.objects.all()
    return render(request, "customer_view_free_album.html", {"album": album})


def customer_view_free_song(request, id):
    song = FreeSong.objects.filter(album_id=id)
    return render(request, "customer_view_free_song.html", {"song": song})


def customer_view_login_free_album(request):
    albums = FreeAlbum.objects.all()
    return render(request, "customer_view_login_free_album.html", {"albums": albums})


def customer_view_login_free_song(request):
    albums = FreeAlbum.objects.all()
    return render(request, "customer_view_login_free_song.html", {"albums": albums})

def search(request):
    if request.method == 'POST':
        title = request.POST["title"]
        count = Album.objects.filter(title=title)
        return render(request, 'customer_view_album.html', {'album': count})
    return render(request, 'customer_view_album.html', {})


# <------------------------------------ Playlist Management ------------------------------------>
def customer_playlist(request):
    # Safely redirects any old playlist links to the new folder system
    return redirect('my_playlists')

def my_playlists(request):
    if not has_active_subscription(request):
        messages.warning(request, "Premium Feature: Subscribe to create custom playlists.")
        return redirect('customer_view_plans')

    email = request.session.get('email')

    if request.method == 'POST':
        playlist_name = request.POST.get('playlist_name')
        if playlist_name:
            UserPlaylist.objects.create(customer_email=email, name=playlist_name)
            return redirect('my_playlists')

    folders = UserPlaylist.objects.filter(customer_email=email).order_by('-created_at')
    return render(request, "my_playlists.html", {"folders": folders})


def view_playlist_songs(request, folder_id):
    if not has_active_subscription(request):
        return redirect('customer_view_plans')

    email = request.session.get('email')
    folder = get_object_or_404(UserPlaylist, id=folder_id, customer_email=email)

    playlist_items = Playlist.objects.filter(user_playlist=folder).select_related('song')

    return render(request, "customer_playlist.html", {
        "playlist_items": playlist_items,
        "folder": folder
    })


def add_to_playlist(request, id):
    if not has_active_subscription(request):
        messages.warning(request, "Premium Feature: You need an active subscription to add songs to your playlist.")
        return redirect('customer_view_plans')

    # Fetch the song early so we can use its album ID for the fallback redirect
    song = get_object_or_404(Song, id=id)

    if request.method == 'POST':
        email = request.session.get('email')
        folder_id = request.POST.get('playlist_id')

        if folder_id and email:
            folder = get_object_or_404(UserPlaylist, id=folder_id, customer_email=email)
            Playlist.objects.get_or_create(customer_email=email, song=song, user_playlist=folder)
            messages.success(request, f"Added to {folder.name}!")

    previous_url = request.META.get('HTTP_REFERER')
    if previous_url:
        return redirect(previous_url)

    # Bulletproof fallback: Always go back to the album if referer is missing
    return redirect('/customer_view_song/{}'.format(song.album.id))


def remove(request, id):
    email = request.session.get('email')
    if email:
        Playlist.objects.filter(id=id, customer_email=email).delete()
        messages.success(request, "Song removed from playlist.")

    previous_url = request.META.get('HTTP_REFERER')
    return redirect(previous_url if previous_url else '/my_playlists')


def customer_playlist_play(request, id):
    if not has_active_subscription(request):
        messages.warning(request, "Premium Feature: You need an active subscription to play these songs.")
        return redirect('customer_view_plans')

    song = get_object_or_404(Song, id=id)
    return render(request, 'customer_playlist_play.html', {'song': song})

# --- Subscriptions & Plans ---
def customer_view_plans(request):
    plans = Subscription.objects.all()
    return render(request, "customer_view_plans.html", {"plans": plans})


from django.core.mail import send_mail  # Ensure this is imported at the top of your file
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta


# ... (your other imports like Customer, Subscription, Subscribers, SubscribersForm)

def buy_plan(request, id):
    email = request.session.get('email')
    plans = get_object_or_404(Subscription, id=id)
    customer = get_object_or_404(Customer, email=email)

    active_subscriptions = Subscribers.objects.filter(customer_email=email, enddate__gte=timezone.now().date())
    if active_subscriptions.exists():
        return render(request, 'buy_plan.html', {
            "message": "Already subscribed to this plan. Enjoy your current subscription!",
            "plans": plans,
            'email': email,
            'startdate': timezone.now().date(),
            'enddate': timezone.now().date() + timedelta(days=plans.months * 30)
        })

    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=plans.months * 30)

    if request.method == "POST":
        form = SubscribersForm(request.POST)
        if form.is_valid():
            new_subscription = form.save(commit=False)
            new_subscription.customer_email = email
            new_subscription.subscription = plans
            new_subscription.startdate = start_date
            new_subscription.enddate = end_date
            new_subscription.save()

            customer.startdate = start_date
            customer.enddate = end_date
            customer.save()

            # ==========================================
            # EMAIL INTEGRATION START
            # ==========================================
            subject = 'Subscription Successful - Welcome to Premium!'
            # You can customize the message to include plan details and dates
            message = f'''Hello {customer.fullname},

Thank you for upgrading your account! Your subscription has been successfully activated.

Plan Details:
- Start Date: {start_date}
- End Date: {end_date}

Enjoy your unlimited music experience!
'''
            from_email = 'your_email@gmail.com'  # Ensure this matches your settings.py
            recipient_list = [email]

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            except Exception as email_error:
                # Log the error but don't break the application flow
                print(f"Subscription saved, but email failed to send: {email_error}")
            # ==========================================
            # EMAIL INTEGRATION END
            # ==========================================

            return render(request, 'buy_plan.html', {
                "message": "Thank you for subscribing! A confirmation email has been sent.",
                "plans": plans,
                'email': email,
                'startdate': start_date,
                'enddate': end_date
            })
        else:
            print(form.errors)

    return render(request, 'buy_plan.html', {
        "plans": plans,
        'email': email,
        'startdate': start_date,
        'enddate': end_date
    })
def customer_view_history(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')

    subscriptions = Subscribers.objects.filter(customer_email=email).select_related('subscription')
    today = timezone.now().date()
    return render(request, "customer_view_history.html", {
        "subscriptions": subscriptions,
        "today": today
    })

# --- Keywords for ML ---
def add_keyword(request):
    email = request.session.get('email')
    if not email:
        return redirect('customer_login')  # Security fallback if session expired

    if request.method == "POST":
        form = KeywordForm(request.POST)
        keyword = request.POST.get("keyword")

        # FIX: Check if this specific keyword already exists FOR THIS USER
        if Keyword.objects.filter(keyword=keyword, email=email).exists():
            return render(request, "add_keyword.html", {"msg": "You have already added this keyword!", 'email': email})

        if form.is_valid():
            try:
                # Commit=False allows us to inject the logged-in user's email before saving to the database
                keyword_instance = form.save(commit=False)
                keyword_instance.email = email
                keyword_instance.save()

                return redirect("/view_keyword")
            except Exception as e:
                print(e)
                return render(request, "add_keyword.html", {"msg": "Keyword Not Added", 'email': email})
        else:
            return render(request, "add_keyword.html",
                          {"msg": "Form is invalid", "form_errors": form.errors, 'email': email})

    return render(request, "add_keyword.html", {'email': email})

def view_keyword(request):
    email = request.session.get('email')
    keyword = Keyword.objects.filter(email=email)
    return render(request, "view_keyword.html", {"cat": keyword})

def delete_keyword(request, id):
    cat = Keyword.objects.get(id=id)
    cat.delete()
    return redirect('/view_keyword')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            # Check if customer exists
            customer = Customer.objects.get(email=email)

            # Generate OTP
            otp = str(random.randint(100000, 999999))

            # Store in session specifically for password reset
            request.session['reset_email'] = email
            request.session['reset_otp'] = otp

            # Send Email
            subject = 'Password Reset OTP'
            message = f'Hello {customer.fullname},\n\nYour One-Time Password (OTP) to reset your password is: {otp}\n\nIf you did not request this, please ignore this email.'
            from_email = 'your_email@gmail.com'
            recipient_list = [email]

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                messages.success(request, f"An OTP has been sent to {email}")
                return redirect('verify_reset_otp')
            except Exception as e:
                print(f"Email failed: {e}")
                messages.error(request, "Failed to send OTP email. Please try again.")
                return render(request, 'forgot_password.html')

        except Customer.DoesNotExist:
            # For security, you can show a generic message even if the email doesn't exist
            messages.error(request, "If this email is registered, an OTP has been sent.")
            return render(request, 'forgot_password.html')

    return render(request, 'forgot_password.html')


# Step 2: Verify the OTP
def verify_reset_otp(request):
    # Ensure user came from step 1
    if 'reset_email' not in request.session:
        return redirect('forgot_password')

    email = request.session['reset_email']

    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('reset_otp')

        if user_otp == session_otp:
            # OTP is correct, allow them to set a new password
            messages.success(request, "OTP Verified. Please enter your new password.")
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'verify_reset_otp.html', {'email': email})


# Step 3: Set the New Password
def reset_password(request):
    # Ensure user has successfully passed the OTP step
    if 'reset_email' not in request.session or 'reset_otp' not in request.session:
        return redirect('forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            email = request.session['reset_email']
            customer = Customer.objects.get(email=email)

            # Update password
            customer.password = new_password
            customer.save()

            # Clean up session variables
            del request.session['reset_email']
            del request.session['reset_otp']

            messages.success(request, "Your password has been successfully reset. Please log in.")
            return redirect('customer_login')
        else:
            messages.error(request, "Passwords do not match. Please try again.")

    return render(request, 'reset_password.html')


def customer_listening_history(request):
    # Get the logged-in user's email
    email = request.session.get('email')

    if not email:
        return redirect('customer_login')  # Redirect to login if session expired

    # Fetch history for this user, newest first
    # (The model's Meta ordering already handles the sorting, but we filter by email)
    listening_history = CustomerListenHistory.objects.filter(customer_email=email)

    return render(request, "customer_listening_history.html", {"history": listening_history})


from django.db.models import Q
from .models import Keyword, Song, FreeSong, CustomerListenHistory


def recommended_songs(request):
    email = request.session.get('email')

    if not email:
        return redirect('customer_login')

    # ==========================================
    # 1. KEYWORD-BASED RECOMMENDATIONS
    # ==========================================
    user_keywords = Keyword.objects.filter(email=email).values_list('keyword', flat=True)
    keyword_premium_songs = []
    keyword_free_songs = []

    if user_keywords:
        search_query = Q()
        for kw in user_keywords:
            search_query |= Q(title__icontains=kw)
            search_query |= Q(singer__icontains=kw)
            search_query |= Q(category__icontains=kw)
            search_query |= Q(album__title__icontains=kw)

        keyword_premium_songs = Song.objects.filter(search_query).distinct()
        keyword_free_songs = FreeSong.objects.filter(search_query).distinct()

    # ==========================================
    # 2. HISTORY-BASED RECOMMENDATIONS
    # ==========================================
    user_history = CustomerListenHistory.objects.filter(customer_email=email)
    history_premium_songs = []
    history_free_songs = []
    favorite_singers = set()
    favorite_categories = set()

    if user_history.exists():
        favorite_singers = set(user_history.values_list('singers', flat=True))
        favorite_categories = set(user_history.values_list('category', flat=True))
        favorite_singers.discard("Unknown Singer")
        favorite_categories.discard("Unknown Category")

        listened_premium_ids = user_history.filter(song_type='premium').values_list('song_id', flat=True)
        listened_free_ids = user_history.filter(song_type='free').values_list('song_id', flat=True)

        hist_query = Q()
        if favorite_singers:
            hist_query |= Q(singer__in=favorite_singers)
        if favorite_categories:
            hist_query |= Q(category__in=favorite_categories)

        if hist_query:
            history_premium_songs = Song.objects.filter(hist_query).exclude(id__in=listened_premium_ids).distinct()[:10]
            history_free_songs = FreeSong.objects.filter(hist_query).exclude(id__in=listened_free_ids).distinct()[:10]

    # Pass all the data to the template
    return render(request, 'recommended_songs.html', {
        # Keyword Data
        'keyword_premium_songs': keyword_premium_songs,
        'keyword_free_songs': keyword_free_songs,
        'keywords': list(user_keywords),

        # History Data
        'history_premium_songs': history_premium_songs,
        'history_free_songs': history_free_songs,
        'singers': list(favorite_singers),
        'categories': list(favorite_categories),
        'has_history': user_history.exists()
    })


import json
import base64
import numpy as np
import cv2
from deepface import DeepFace
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Song


@csrf_exempt
def emotion_recommendation(request):
    if request.method == 'POST':
        try:
            # 1. Parse the incoming image from the webcam
            data = json.loads(request.body)
            image_data = data.get('image')

            # 2. Decode the Base64 string into an OpenCV image array
            encoded_data = image_data.split(',')[1]
            nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # --- NEW SAFETY CHECK ---
            if img is None:
                return JsonResponse({'status': 'error', 'message': 'The camera sent a blank image. Please try again.'})
            # ------------------------

            # 3. Run the ML Emotion Detection
            results = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
            emotion = results[0]['dominant_emotion'] if isinstance(results, list) else results['dominant_emotion']

            # 4. Map Emotions to your Database Categories
            emotion_map = {
                'happy': 'Melody',
                'sad': 'folk',
                'angry': 'Rock',
                'neutral': 'Mass',
                'surprise': 'Electronic',
                'fear': 'Ambient',
                'disgust': 'Metal'
            }
            target_category = emotion_map.get(emotion.lower(), 'Pop')

            # 5. Fetch 3 random matching songs from that category
            songs = Song.objects.filter(category__icontains=target_category).order_by('?')[:3]

            # 6. Serialize the data
            song_list = [{'id': s.id, 'title': s.title, 'singer': s.singer, 'image': s.album.image.url} for s in songs]

            return JsonResponse(
                {'status': 'success', 'emotion': emotion, 'category': target_category, 'songs': song_list})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def ai_mood_matcher(request):
    # Optional: Block free users from using the AI feature
    if not has_active_subscription(request):
        messages.warning(request, "Premium Feature: Subscribe to use the AI Mood Matcher.")
        return redirect('customer_view_plans')

    return render(request, 'emotion_camera.html')