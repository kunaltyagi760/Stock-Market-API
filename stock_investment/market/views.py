from django.http import Http404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AddMoney, Stock, Transaction, PurchasedStock

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from .serializer import (
    RegisterSerializer,
    AddMoneySerializer,
    StockSerializer,
    TransactionSerializer,
    PurchasedStockSerializer
)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddMoneyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return AddMoney.objects.get(user=self.request.user)
        except AddMoney.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        addmoney = self.get_object()
        serializer = AddMoneySerializer(addmoney)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        addmoney = self.get_object()
        serializer = AddMoneySerializer(addmoney, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Stock.objects.get(pk=pk)
        except Stock.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        stock = self.get_object(pk)
        serializer = StockSerializer(stock)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        stock = self.get_object(pk)
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        stock = self.get_object(pk)
        stock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TransactionListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TransactionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk, user=self.request.user)
        except Transaction.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

class PurchasedStockListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        purchased_stocks = PurchasedStock.objects.filter(user=request.user)
        serializer = PurchasedStockSerializer(purchased_stocks, many=True)
        return Response(serializer.data)
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Option 1: Get the refresh token from the request body
            refresh_token = request.data.get("refresh_token")

            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Validate and blacklist the refresh token
            token = RefreshToken(refresh_token)

            # Ensure the token belongs to the user making the request
            if str(token.payload.get('user_id')) != str(request.user.id):
                return Response({"error": "Invalid token for this user"}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the refresh token
            token.blacklist()

            return Response({"message": "Logout successful!"}, status=status.HTTP_205_RESET_CONTENT)
        except (TokenError, InvalidToken) as e:
            return Response({"error": f"Token error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)




           

# Create your views here.
