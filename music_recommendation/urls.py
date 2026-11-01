"""crime_occurrence_prediction URL Configuration"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from music_recommendationapp import views

urlpatterns = [
    # ==========================================
    # DJANGO DEFAULT ADMIN
    # ==========================================
    path('admin/', admin.site.urls),

    # ==========================================
    # COMMON / PUBLIC URLS
    # ==========================================
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('play_song/<int:id>', views.play_song, name='play_song'),

    # ==========================================
    # CUSTOMER URLS
    # ==========================================
    # Authentication & Profile
    path('customer_registration', views.customer_registration, name="customer_registration"),
    path('customer_login/', views.customer_login, name="customer_login"),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('customer_logout', views.customer_logout, name="customer_logout"),
    path('customer_change_password', views.customer_change_password, name="customer_change_password"),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_reset_otp/', views.verify_reset_otp, name='verify_reset_otp'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('customer_home', views.customer_home, name="customer_home"),
    path('customer_profile', views.customer_profile, name="customer_profile"),
    path('customer_edit/<int:id>', views.customer_edit, name="customer_edit"),
    path('customer_update', views.customer_update, name="customer_update"),
    path('customer_listening_history', views.customer_listening_history, name="customer_listening_history"),
    path('admin_update_customer_status/<int:id>/<str:status>/', views.admin_update_customer_status, name="admin_update_customer_status"),

    # Content Viewing (Premium)
    path('customer_view_album', views.customer_view_album, name="customer_view_album"),
    path('customer_view_song/<int:id>', views.customer_view_song, name="customer_view_song"),
    path('customer_view_song_play/<int:id>', views.customer_view_song_play, name='customer_view_song_play'),
    path('search', views.search, name="search"),

    # Content Viewing (Free)
    path('customer_view_login_free_album', views.customer_view_login_free_album, name="customer_view_login_free_album"),
    path('customer_view_login_free_song/<int:id>', views.customer_view_login_free_song, name="customer_view_login_free_song"),
    path('customer_view_free_album', views.customer_view_free_album, name="customer_view_free_album"),
    path('customer_view_free_song/<int:id>', views.customer_view_free_song, name="customer_view_free_song"),

    # Playlists
    path('add_to_playlist/<int:id>', views.add_to_playlist, name="add_to_playlist"),
    path('customer_playlist', views.customer_playlist, name="customer_playlist"),
    path('customer_playlist/<int:id>', views.customer_playlist, name="customer_playlist_id"),
    path('customer_playlist_play/<int:id>', views.customer_playlist_play, name='customer_playlist_play'),
    path('remove/<int:id>', views.remove, name="remove"),

    # Subscriptions & Plans
    path('customer_view_plans', views.customer_view_plans, name="customer_view_plans"),
    path('buy_plan/<int:id>', views.buy_plan, name="buy_plan"),
    path('customer_view_history/', views.customer_view_history, name='customer_view_history'),

    # ML Recommendation Features
    path('home/', views.home, name="home"),
    path('add_keyword', views.add_keyword, name="add_keyword"),
    path('view_keyword', views.view_keyword, name="view_keyword"),
    path('delete_keyword/<int:id>', views.delete_keyword, name="delete_keyword"),


    # ==========================================
    # ADMIN URLS
    # ==========================================
    # Authentication
    path('admin_login/', views.admin_login, name="admin_login"),
    path('admin_logout', views.admin_logout, name="admin_logout"),
    path('admin_change_password', views.admin_change_password, name="admin_change_password"),
    path('admin_home', views.admin_home, name="admin_home"),

    # User Management
    path('view_customer', views.view_customer, name="view_customer"),
    path('admin_delete_customer/<int:id>', views.admin_delete_customer, name="admin_delete_customer"),
    path('view_contact', views.view_contact, name="view_contact"),
    path('admin_view_subscribers', views.admin_view_subscribers, name="admin_view_subscribers"),

    # Premium Content Management
    path('add_album', views.add_album, name="add_album"),
    path('view_album', views.view_album, name="view_album"),
    path('edit_album/<int:id>', views.edit_album, name="edit_album"),
    path('update_album', views.update_album, name="update_album"),
    path('delete_album/<int:id>', views.delete_album, name="delete_album"),

    path('add_song/<int:id>', views.add_song, name="add_song"),
    path('view_song/<int:id>', views.view_song, name="view_song"),
    path('edit_song/<int:id>', views.edit_song, name="edit_song"),
    path('update_song', views.update_song, name="update_song"),
    path('delete_song/<int:id>', views.delete_song, name="delete_song"),
    path('admin_view_play_song/<int:id>', views.admin_view_play_song, name='admin_view_play_song'),

    # Free Content Management
    path('add_free_album/', views.add_free_album, name="add_free_album"),
    path('view_free_album', views.view_free_album, name="view_free_album"),
    path('free_edit_album/<int:id>', views.free_edit_album, name="free_edit_album"),
    path('free_update_album', views.free_update_album, name="free_update_album"),
    path('free_delete_album/<int:id>', views.free_delete_album, name="free_delete_album"),

    path('add_free_song/<int:id>', views.add_free_song, name="add_free_song"),
    path('view_free_song/<int:id>', views.view_free_song, name="view_free_song"),
    path('free_edit_song/<int:id>', views.free_edit_song, name="free_edit_song"),
    path('free_update_song', views.free_update_song, name="free_update_song"),
    path('free_delete_song/<int:id>', views.free_delete_song, name="free_delete_song"),
    path('admin_view_free_play_song/<int:id>', views.admin_view_free_play_song, name='admin_view_free_play_song'),

    # Categories
    path('add_category/', views.add_category, name="add_category"),
    path('view_category/', views.view_category, name="view_category"),
    path('delete_category/<int:id>', views.delete_category, name="delete_category"),

    # Subscription Plans
    path('add_plan', views.add_plan, name="add_plan"),
    path('view_plan', views.view_plan, name="view_plan"),
    path('plan_delete/<int:id>', views.plan_delete, name="plan_delete"),
    path('recommended_songs/', views.recommended_songs, name='recommended_songs'),
    path('my_playlists/', views.my_playlists, name='my_playlists'),
    path('view_playlist_songs/<int:folder_id>/', views.view_playlist_songs, name='view_playlist_songs'),
    path('emotion_recommendation/', views.emotion_recommendation, name='emotion_recommendation'),
path('ai_mood_matcher/', views.ai_mood_matcher, name='emotion_camera'),    # path('history_recommendations/', views.history_recommendations, name='history_recommendations'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)