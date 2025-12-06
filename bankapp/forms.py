from django import forms

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
