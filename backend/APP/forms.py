
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from APP.models import details
class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']



class Loginform(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput)


# class UserDetailsForm():
#     username = forms.CharField(widget=TextInput)
#     email = forms.EmailField(widget=TextInput)
#     img = forms.ImageField()

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = details
        fields = ['username', 'email', 'img']

    def clean_email(self):
        email = self.cleaned_data['email']
        # Add any custom email validation logic here, if needed
        return email
