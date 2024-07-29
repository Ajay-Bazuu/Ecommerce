from django import forms
from .models import Profile, User,Review

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        db_table = 'Profile'
        fields= ['user', 'profile_picture', 'phone_number', 'address']
        widgets={
            'profile_picture':forms.FileInput(attrs={'class':'form-control'}),
            'phone_number':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your phone number.'}),
            'address':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your address.'}),
        }

class ReviewForm(forms.ModelForm):
    class  Meta:
        model=Review
        fields=['comment','rating']
        widgets={
            'rating':forms.Select(choices=[(i,i) for i in range(1,6)],attrs={'class':'form-control'}),
            'comment':forms.Textarea(attrs={'class':'form-control','placeholder':'Comment'})
        }


