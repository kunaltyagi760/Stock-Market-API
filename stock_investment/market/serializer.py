from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AddMoney, Stock, Transaction, PurchasedStock

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        AddMoney.objects.create(user=user, balance=0)  # Create a wallet for the user with a balance of zero
        return user

class AddMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddMoney
        fields = ['user', 'balance']
        read_only_fields = ['user']

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['symbol', 'name', 'current_price']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'stock', 'transaction_type', 'quantity', 'price', 'timestamp']
        read_only_fields = ['user', 'price', 'timestamp']

    def validate(self, data):
        user = self.context['request'].user
        stock = data['stock']
        quantity = data['quantity']
        transaction_type = data['transaction_type']
        price = stock.current_price

        if transaction_type == 'BUY':
            if user.wallet.balance < quantity * price:
                raise serializers.ValidationError("Insufficient balance for this transaction.")
        elif transaction_type == 'SELL':
            purchased_stock = PurchasedStock.objects.filter(user=user, stock=stock).first()
            if not purchased_stock or purchased_stock.quantity < quantity:
                raise serializers.ValidationError("Insufficient stocks for this transaction.")
        return data

class PurchasedStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedStock
        fields = ['user', 'stock', 'quantity']
        read_only_fields = ['user', 'stock']



