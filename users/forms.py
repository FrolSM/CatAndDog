from allauth.account.forms import SignupForm
from django import forms


class MyCustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].widget.attrs['placeholder'] = 'Имя пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'

    def save(self, request):
        user = super().save(request)

        return user

    def clean_username(self):
        username = self.cleaned_data['username']
        if 'admin' in username.lower():
            raise forms.ValidationError('Недопустимое имя пользователя')
        return username
