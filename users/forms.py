from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User




class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=False)
    phone = forms.CharField(max_length=20, required=False, label='Phone Number')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Username', 'first_name': 'First name', 'last_name': 'Last name (optional)',
            'email': 'Email address', 'phone': 'Phone number (optional)',
            'password1': 'Password', 'password2': 'Confirm password',
        }
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control auth-input', 'placeholder': placeholders.get(name, '')})

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Username"
        })

        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Password"
        })
