
from django.shortcuts import render,redirect, get_object_or_404
from .forms import PostForm,UserRegisterForm,LoginForm,EditProfileForm,ChangePasswordForm,SearchUserform
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .models import User,Post
from friends.models import FriendRequest,FriendList
from django.views.decorators.csrf import csrf_exempt
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('accounts:index.html')

    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
@login_required
def home_view(request):
    user = request.user
    try:
        friend_list = FriendList.objects.get(user=user)
        friends = friend_list.friends.all() 
    except FriendList.DoesNotExist:
        friends = []

    posts = Post.objects.filter(user__in=[user, *friends]).order_by('-created_at')

    return render(request, 'accounts/index.html', {'posts': posts})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    return redirect('accounts:home')

                else:
                    form.add_error('password', 'Invalid password') 
            except User.DoesNotExist:
                form.add_error('email', 'User not found')  
    
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def current_profile_view(request):
    profile_user = request.user 
    return render(request, 'accounts/profile.html', {'user': profile_user})

@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login') 
def profile_view(request, user_id):
    try:
        profile_user = User.objects.get(user_id=user_id)  

        logged_in_user = request.user

        logged_in_user_friend_list, created = FriendList.objects.get_or_create(user=logged_in_user)
        
        are_friends = logged_in_user_friend_list.is_friend(profile_user)
        
        sent_request = FriendRequest.objects.filter(sender=logged_in_user, receiver=profile_user, active_status=True).exists()
        received_request = FriendRequest.objects.filter(sender=profile_user, receiver=logged_in_user, active_status=True).exists()

        return render(request, 'accounts/profile.html', {
            'user': profile_user,
            'are_friends': are_friends,
            'sent_request': sent_request,
            'received_request': received_request,
        })
    
    except User.DoesNotExist:
        return render(request, 'accounts/profile.html', {'error': 'User not found'})

@login_required
def edit_profile(request):
    form = EditProfileForm(request.POST or None, request.FILES or None, instance=request.user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('accounts:profile') 

    return render(request, 'accounts/edit_profile.html', {'form': form})

def edit_password(request):
    if request.method == 'POST': 
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            newpassword = form.cleaned_data['newpassword']
            print(f"Email: {email}, Password: {password}, New Password: {newpassword}")

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                form.add_error('email', 'Email not found')
                return render(request, 'accounts/changepassword.html', {'form': form})
            if user.check_password(password):
                user.set_password(newpassword)
                user.save()
                return redirect('accounts:home')

            else:
                form.add_error('password', 'Invalid password')             
    else:
        form = ChangePasswordForm()
    return render(request, 'accounts/changepassword.html', {'form': form})
@login_required
def search_users(request):
    if request.method == 'POST':
        form = SearchUserform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                results = User.objects.filter(username__icontains=username)
                return render(request, 'accounts/search_users.html', {'results': results, 'form': form})
            except User.DoesNotExist:
                return render(request, 'accounts/search_users.html', {'results': [], 'form': form})
    else:
        form = SearchUserform()

    return render(request, 'accounts/search_users.html', {'form': form, 'results': []})
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('accounts:home')  
    else:
        form = PostForm()
    return render(request, 'accounts/create_post.html', {'form': form})

@login_required
def show_friendlist(request):
    user = request.user
    try:
        friend_list = FriendList.objects.get(user=user)
        friends = friend_list.get_friends()
    except FriendList.DoesNotExist:
        friends = []
    return render(request, 'accounts/friendlist.html', {'friends': friends})
