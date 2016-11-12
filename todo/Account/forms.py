from django import forms
from django.contrib.auth import authenticate,get_user_model
User=get_user_model()
class LoginForm(forms.Form):
    username= forms.CharField(label='username', max_length=255)
    password= forms.CharField(label='password',max_length=255,widget=forms.PasswordInput)

    def clean(self,*args,**kwargs):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')
        if username and password:
            user_obj=User.objects.filter(username=username)
            if not user_obj.exists():
                raise forms.ValidationError("Please Enter correct username")
            elif not user_obj[0].check_password(password):
                raise forms.ValidationError("Please Enter the correct password")
            elif not user_obj[0].is_active:
                raise forms.ValidationError("User is not active contact to your admin")
        else:
            raise forms.ValidationError("Please fill the login info")
        return super(LoginForm,self).clean(*args,**kwargs)
