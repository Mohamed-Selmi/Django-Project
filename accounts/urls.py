from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
app_name = 'accounts'
urlpatterns = [
	path('register/', register_view, name='register'),
    path('', home_view, name='home'),
    path('login/', login_view, name='login'), 
    path('profile/<int:user_id>/', profile_view, name='profile_detail'),
    path('edit/', edit_profile, name='edit_profile'),
    path('profile/', current_profile_view, name='profile'),
    path('changepass/', edit_password, name='changepass'),
    path('search/', search_users, name='search_users'),
    path('create_post/', create_post, name='create_post'),
    path('logout/', logout_view, name='logout'),
    path('friendlist/', show_friendlist, name='show_friendlist'),

]