from django.urls import path
from .views import *
app_name = 'friends'

urlpatterns = [
    path('send_request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('friend_requests/', show_friend_requests, name='show_friend_requests'),
    path('cancel_request/<int:friend_request_id>/',cancel_friend_request, name='cancel_friend_request'),
    path('accept_request/<int:friend_request_id>/', accept_friend_request, name='accept_friend_request'),
    path('decline_request/<int:friend_request_id>/',decline_friend_request, name='decline_friend_request'),
]
