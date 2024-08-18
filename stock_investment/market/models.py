from django.contrib.auth.models import User
from django.db import models
from django.db.models import F

class AddMoney(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.user}-{self.balance}'

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.name}-{self.current_price}'

class PurchasedStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stocks')
    stock = models.ForeignKey(Stock, null=True, on_delete=models.CASCADE, related_name='owners')
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user}-{self.stock}'

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    stock = models.ForeignKey(Stock, null=True, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=(('BUY', 'Buy'), ('SELL', 'Sell')))
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.price = self.stock.current_price * self.quantity
        super().save(*args, **kwargs)
        if self.transaction_type == 'BUY':
            self.user.wallet.balance = F('balance') - self.price
            purchased_stock, created = PurchasedStock.objects.get_or_create(
                user=self.user,
                stock=self.stock,
                defaults={'quantity': 0}
            )
            purchased_stock.quantity = F('quantity') + self.quantity
            purchased_stock.save()
        elif self.transaction_type == 'SELL':
            self.user.wallet.balance = F('balance') + self.price
            purchased_stock = PurchasedStock.objects.get(user=self.user, stock=self.stock)
            purchased_stock.quantity = F('quantity') - self.quantity
            purchased_stock.save()
            # Refresh purchased_stock from the database to get the updated quantity
            purchased_stock.refresh_from_db()
            if purchased_stock.quantity == 0:
                purchased_stock.delete()
        self.user.wallet.save()

    def __str__(self):
        return f'{self.user}-{self.transaction_type}'







# Create your models here.
