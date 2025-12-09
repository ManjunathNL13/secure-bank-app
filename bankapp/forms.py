from django import forms
from .models import Account

class LoginForm(forms.Form):
    acc_number = forms.CharField(
        label="Account Number", 
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter account number'})
    )
    pin = forms.CharField(
        label="PIN", 
        max_length=10, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter PIN'})
    )

class DepositForm(forms.Form):
    amount = forms.DecimalField(
        label="Amount (₹)", 
        max_digits=12, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount', 'min': '0', 'step': '0.01'})
    )

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(
        label="Amount (₹)", 
        max_digits=12, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount', 'min': '0', 'step': '0.01'})
    )
    pin = forms.CharField(
        label="Confirm PIN", 
        max_length=10, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your PIN'})
    )

class RegistrationForm(forms.ModelForm):
    confirm_pin = forms.CharField(
        label="Confirm PIN", 
        max_length=10, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm PIN'})
    )
    
    class Meta:
        model = Account
        fields = ['acc_number', 'name', 'pin']
        widgets = {
            'acc_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter account number'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'pin': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter PIN'}),
        }
        labels = {
            'acc_number': 'Account Number',
            'name': 'Full Name',
            'pin': 'PIN',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get('pin')
        confirm_pin = cleaned_data.get('confirm_pin')
        
        if pin and confirm_pin and pin != confirm_pin:
            raise forms.ValidationError("PIN and Confirm PIN do not match")
        
        return cleaned_data