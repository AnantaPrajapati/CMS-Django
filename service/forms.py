from django import forms
from .models import Notice, User
# from django.contrib.auth.models import User

class NoticeForm(forms.Form):
    class Meta:
        model = Notice 
        field = [ 'image', 'title', 'description', ]

class AdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, commit = True):
        user = super().save(commit= False)
        user.set_password(self.cleaned_data["password"])
        user.is_staff =True
        if commit:
            user.save()
        return user

