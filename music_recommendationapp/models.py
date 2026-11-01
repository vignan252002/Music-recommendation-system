from django.db import models


# Create your models here.


class Customer(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    mobile = models.BigIntegerField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.IntegerField()
    status = models.CharField(max_length=50, default="pending", null=True)

    class Meta:
        db_table = 'Customer'


class Admin(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'Admin'


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    class Meta:
        db_table = 'Contact'


class Album(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=100)
    production = models.CharField(max_length=100)
    image = models.ImageField()
    tracks = models.IntegerField()
    language = models.CharField(max_length=100)
    year = models.IntegerField()

    class Meta:
        db_table = 'Album'


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    singer = models.CharField(max_length=1000)
    file = models.FileField()
    category = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="pending", null=True)

    class Meta:
        db_table = 'Song'


class Category(models.Model):
    category = models.CharField(max_length=100)

    class Meta:
        db_table = 'Category'

class Keyword(models.Model):
    email = models.EmailField()
    keyword = models.CharField(max_length=100)

    class Meta:
        db_table = 'Keyword'


#
# class Subscribe(models.Model):
#     email = models.EmailField()
#     start_date = models.DateField()
#     end_date = models.DateField()
#     package = models.CharField(max_length=100)
#     price = models.BigIntegerField()
#     status = models.CharField(max_length=20, default='active')  # Status field to track activation/deactivation
#
#
#     class Meta:
#         db_table = 'Subscribe'

class FreeAlbum(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=100)
    production = models.CharField(max_length=100)
    image = models.ImageField()
    tracks = models.IntegerField()
    language = models.CharField(max_length=100)
    year = models.IntegerField()

    class Meta:
        db_table = 'FreeAlbum'


class FreeSong(models.Model):
    album = models.ForeignKey(FreeAlbum, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    singer = models.CharField(max_length=100)
    file = models.FileField()
    category = models.CharField(max_length=100)
    director = models.CharField(max_length=100)

    class Meta:
        db_table = 'FreeSong'


class Subscription(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=100)
    months = models.IntegerField()
    cost = models.BigIntegerField()
    discount = models.BigIntegerField()
    date_time = models.DateTimeField(auto_now=True)


class Subscribers(models.Model):
    customer_email = models.EmailField()
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    startdate = models.DateField()
    enddate = models.DateField()
    holder_name = models.CharField(max_length=100)
    card_number = models.BigIntegerField()
    cvv_number = models.BigIntegerField()
    bank_name = models.CharField(max_length=100)


class CustomerListenHistory(models.Model):
    customer_email = models.EmailField()

    # Adding clean defaults for existing and future rows
    song_id = models.IntegerField(default=0)
    album_id = models.IntegerField(default=0)
    song_title = models.CharField(max_length=200, default="Unknown Title")

    # NEW FIELDS ADDED HERE
    singers = models.CharField(max_length=1000, default="Unknown Singer")
    category = models.CharField(max_length=100, default="Unknown Category")

    song_type = models.CharField(max_length=10, default="unknown")

    listened_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CustomerListenHistory'
        ordering = ['-listened_at']

    def __str__(self):
        return f"{self.customer_email} listened to {self.song_title} by {self.singers} at {self.listened_at}"


class UserPlaylist(models.Model):
    customer_email = models.EmailField()
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'UserPlaylist'

    def __str__(self):
        return f"{self.name} ({self.customer_email})"


class Playlist(models.Model):
    customer_email = models.EmailField()
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    # Links the song to the specific custom folder
    user_playlist = models.ForeignKey(UserPlaylist, on_delete=models.CASCADE, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Playlist'
        # Ensures a user can't add the SAME song to the SAME folder twice
        unique_together = ('user_playlist', 'song')

    def __str__(self):
        return f"{self.customer_email} - {self.song.title}"