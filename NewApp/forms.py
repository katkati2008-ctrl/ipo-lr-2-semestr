from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        help_text='Обязательное поле. Введите действующий адрес электронной почты.'
    )
    city = forms.CharField(max_length=100, required=False, label='Город')
    address = forms.CharField(widget=forms.Textarea, required=False, label='Адрес')


    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            profile = user.profile
            profile.city = self.cleaned_data.get('city', '')
            profile.address = self.cleaned_data.get('address', '')
            profile.save()
        
        return user


