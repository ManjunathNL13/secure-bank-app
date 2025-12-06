from django.db import models

class Account(models.Model):
    acc_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    pin = models.CharField(max_length=10)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.acc_number} - {self.name}"

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    action = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
