from django import forms
from .models import User,Post
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    fields = ['email', 'password']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'picture']  


    def clean_picture(self):
        picture = self.cleaned_data.get('picture')
        if picture:
            if picture.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Profile picture is too large. Max size is 5MB.")
        return picture
    
class ChangePasswordForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    newpassword = forms.CharField(widget=forms.PasswordInput())


class SearchUserform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']
    