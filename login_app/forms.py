from django import forms
from .models import CustomUser
from django.contrib.auth.models import User, Permission

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'phone_number', 'profile_image', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')

        return cleaned_data
    
class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'phone_number', 'profile_image']




class GrantPermissionForm(forms.Form):
    user_id = forms.ChoiceField(choices=[], label="Select User")
    make_superuser = forms.BooleanField(required=False, label="Make Superuser")
    make_staff = forms.BooleanField(required=False, label="Make Staff")
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Permissions"
    )

    def __init__(self, *args, **kwargs):
        super(GrantPermissionForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].choices = [(user.id, user.full_name) for user in CustomUser.objects.all()]
