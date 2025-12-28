from django import forms
from .models import Donation
from django.contrib.auth.models import User
from .models import MemberProfile

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None  # removes the "Required. 150 characters..." message

class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = [
            'first_name', 'middle_name', 'last_name', 'suffix', 'email_address', 
            'relationship_status', 'contact_number', 'birth_date', 'address', 'photo'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'middle_name': forms.TextInput(attrs={'placeholder': 'Middle name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'suffix': forms.TextInput(attrs={'placeholder': 'Suffix (e.g., Jr., Sr.)'}),
            'email_address': forms.EmailInput(attrs={'placeholder': 'Email address'}),
            'relationship_status': forms.Select(choices=MemberProfile.RELATIONSHIP_CHOICES),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Contact number'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Address'}),
        }



class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'method', 'receipt_image']

    # 👇 Add this here (after Meta)
    def __init__(self, *args, **kwargs):
        super(DonationForm, self).__init__(*args, **kwargs)
        # Make the receipt image required
        self.fields['receipt_image'].required = True

    def clean_receipt_image(self):
        img = self.cleaned_data.get('receipt_image')
        if img:
            if img.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError("Receipt too large (max 10MB).")
            ext = img.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png']:
                raise forms.ValidationError("Unsupported file type.")
        else:
            # 👇 This ensures backend also enforces the required rule
            raise forms.ValidationError("Please upload a photo of your payment receipt.")
        return img
