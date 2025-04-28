from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FriendRequest, FriendList
from accounts.models import User

@login_required
def send_friend_request(request, user_id):
    print(request)
    sending_user = request.user
    try:
        receiving_user = User.objects.get(user_id=user_id)

        if FriendRequest.objects.filter(sender=sending_user, receiver=receiving_user, active_status=True).exists():
            messages.error(request, 'Friend request already sent.')
        elif FriendList.objects.get(user=sending_user).is_friend(receiving_user):
            messages.error(request, 'You are already friends with this user.')
        else:
            FriendRequest.objects.create(sender=sending_user, receiver=receiving_user, active_status=True)
            messages.success(request, 'Friend request sent successfully.')

    except User.DoesNotExist:
        messages.error(request, 'User not found.')

    return redirect('accounts:profile_detail', user_id=user_id)  
@login_required
def show_friend_requests(request):
    received_requests = FriendRequest.objects.filter(receiver=request.user, active_status=True)
    sent_requests = FriendRequest.objects.filter(sender=request.user, active_status=True)
    return render(request, 'accounts/show_friend_requests.html', {
        'received_requests': received_requests,
        'sent_requests': sent_requests
    })


@login_required
def accept_friend_request(request, friend_request_id):
    try:
        friend_request = FriendRequest.objects.get(id=friend_request_id, receiver=request.user)
        friend_request.AcceptFriendRequest()
        messages.success(request, 'Friend request accepted successfully.')
    except FriendRequest.DoesNotExist:
        messages.error(request, 'Friend request does not exist.')
    return redirect('friends:show_friend_requests')

@login_required
def decline_friend_request(request, friend_request_id):
    try:
        friend_request = FriendRequest.objects.get(id=friend_request_id, receiver=request.user)
        friend_request.DeclineFriendRequest()
        messages.success(request, 'Friend request declined successfully.')
    except FriendRequest.DoesNotExist:
        messages.error(request, 'Friend request does not exist.')
    return redirect('friends:show_friend_requests')

@login_required
def cancel_friend_request(request,friend_request_id):
    try:
        friend_request = FriendRequest.objects.get(id=friend_request_id, sender=request.user)
        friend_request.CancelFriendRequest()
        messages.success(request, 'Friend request canceled successfully.')
    except FriendRequest.DoesNotExist:
        messages.error(request, 'Friend request does not exist.')
    return redirect('friends:show_friend_requests')
