from django.core.validators import RegexValidator, MinLengthValidator
from django import forms

from .models import CustomUser


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "الاسم الاول",
            "class": "form-control input_email"
        }))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "الاسم الثاني",
            "class": "form-control input_email"
        }))
    email = forms.EmailField(max_length=200, help_text='Required', widget=forms.EmailInput(attrs={
        "placeholder": "البريد الالكتروني",
        "class": "form-control input_email"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "كلمة المرور",
        "class": "form-control input_email"
    }),
        validators=[MinLengthValidator(8, message="Password must be at least 8 characters long.")])

    phone_number = forms.CharField(label="phone number", widget=forms.TextInput(attrs={
        "placeholder": "رقم الهاتف",
        "class": "form-control input_email"
    }))

    def clean(self):
        errors = {}
        user_email = self.cleaned_data.get('user_email')
        if CustomUser.objects.filter(email=user_email).exists():
            errors['user_email'] = ("Email exists")
        phone = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone).exists():
            errors['phone_number'] = ("phone exists")
        if errors:
            raise forms.ValidationError(errors)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',
                  'password', 'phone_number',)


class LoginForm(forms.ModelForm):
    email = forms.EmailField(max_length=200, help_text='Required', widget=forms.EmailInput(attrs={
        "placeholder": "البريد الالكتروني",
        "class": "form-control input_email"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "كلمة المرور",
        "class": "form-control input_email"
    }))

    class Meta:
        model = CustomUser
        fields = ('email',
                  'password',)
