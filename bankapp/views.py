from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
import csv
from .models import Account, Transaction
from .forms import LoginForm, DepositForm, WithdrawForm, RegistrationForm

def index(request):
    context = {
        'is_home_page': True
    }
    return render(request, 'index.html', context)

def about_view(request):
    context = {
        'is_home_page': False
    }
    return render(request, 'about.html', context)

def services_view(request):
    context = {
        'is_home_page': False
    }
    return render(request, 'services.html', context)

def contact_view(request):
    context = {
        'is_home_page': False
    }
    return render(request, 'contact.html', context)

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.balance = 0  # Set initial balance to 0
            account.save()
            return redirect('registration_success')
    else:
        form = RegistrationForm()
    
    context = {
        'form': form,
        'is_home_page': False
    }
    return render(request, 'register.html', context)

def registration_success_view(request):
    context = {
        'is_home_page': False
    }
    return render(request, 'registration_success.html', context)

def login_view(request):
    error = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            acc_number = form.cleaned_data['acc_number']
            pin = form.cleaned_data['pin']
            try:
                acc = Account.objects.get(acc_number=acc_number, pin=pin)
                request.session['acc_number'] = acc.acc_number
                return redirect('dashboard')
            except Account.DoesNotExist:
                error = "Invalid account number or PIN"
    else:
        form = LoginForm()
    context = {
        'form': form, 
        'error': error,
        'is_home_page': False
    }
    return render(request, 'login.html', context)

def dashboard_view(request):
    acc_number = request.session.get('acc_number')
    if not acc_number:
        return redirect('login')
    acc = get_object_or_404(Account, acc_number=acc_number)
    context = {
        'account': acc,
        'is_home_page': False
    }
    return render(request, 'dashboard.html', context)

def deposit_view(request):
    acc_number = request.session.get('acc_number')
    if not acc_number:
        return redirect('login')
    acc = get_object_or_404(Account, acc_number=acc_number)
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount > 0:
                acc.balance += amount
                acc.save()
                Transaction.objects.create(account=acc, action="Deposit", amount=amount)
                context = {
                    'account': acc, 
                    'amount': amount,
                    'is_home_page': False
                }
                return render(request, 'deposit_success.html', context)
            else:
                form.add_error('amount', "Invalid amount!")
    else:
        form = DepositForm()
    context = {
        'form': form, 
        'account': acc,
        'is_home_page': False
    }
    return render(request, 'deposit_form.html', context)

def withdraw_view(request):
    acc_number = request.session.get('acc_number')
    if not acc_number:
        return redirect('login')
    acc = get_object_or_404(Account, acc_number=acc_number)
    if request.method == "POST":
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if 0 < amount <= acc.balance:
                acc.balance -= amount
                acc.save()
                Transaction.objects.create(account=acc, action="Withdraw", amount=amount)
                context = {
                    'account': acc, 
                    'amount': amount,
                    'is_home_page': False
                }
                return render(request, 'withdraw_success.html', context)
            else:
                form.add_error('amount', "Insufficient balance or invalid amount!")
    else:
        form = WithdrawForm()
    context = {
        'form': form, 
        'account': acc,
        'is_home_page': False
    }
    return render(request, 'withdraw_form.html', context)

def mini_statement_view(request):
    acc_number = request.session.get('acc_number')
    if not acc_number:
        return redirect('login')
    acc = get_object_or_404(Account, acc_number=acc_number)
    
    # Check if export is requested
    if 'export' in request.GET:
        # Create the HttpResponse object with CSV header
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="mini_statement_{acc.acc_number}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Date & Time', 'Action', 'Amount'])
        
        last_transactions = acc.transactions.order_by('-timestamp')[:5]
        for transaction in last_transactions:
            writer.writerow([
                transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                transaction.action,
                transaction.amount
            ])
        
        return response
    
    last_transactions = acc.transactions.order_by('-timestamp')[:5]
    context = {
        'account': acc, 
        'transactions': last_transactions,
        'is_home_page': False
    }
    return render(request, 'mini_statement.html', context)

def logout_view(request):
    request.session.flush()
    return redirect('index')