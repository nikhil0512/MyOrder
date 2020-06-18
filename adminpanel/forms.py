import uuid
from django import forms
from adminpanel.models import Store
from django.contrib.auth.models import User


def generate_username():
    """
    Generate a random and unique username using the uuid library
    Also consider uniqueness by comparing with existing user names in db.
    """
    username = uuid.uuid4().hex[:30]
    try:
        while True:
            User.objects.get(username=username)
            username = uuid.uuid4().hex[:30]
    except User.DoesNotExist:
        pass
    return username


class StoreForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = Store
        fields = ('storename', 'pin', 'address')

    def clean(self):
        try:
            email = self.cleaned_data['email'].lower()
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('A user with this email already exists.')
            self.cleaned_data['email'] = email
            return self.cleaned_data
        except (KeyError, ValueError):
            raise forms.ValidationError('Email')

    def save(self, commit=True):
        store_form_object = super(StoreForm, self).save(commit=False)
        store_form_object.user.set_password(self.cleaned_data["password1"])
        store_form_object.user.username = generate_username()
        store_form_object.user.first_name = self.cleaned_data["first_name"].title()
        store_form_object.user.last_name = self.cleaned_data["last_name"].title()
        if commit:
            store_form_object.user.save()
            store_form_object.save()
        return store_form_object

