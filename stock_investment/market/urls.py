from django.urls import path
from .views import (
    RegisterView,
    AddMoneyView,
    StockListCreateView,
    StockDetailView,
    TransactionListCreateView,
    TransactionDetailView,
    PurchasedStockListCreateView,
    LogoutView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Stock Market API",
        default_version='v1',
        description="API documentation for the Stock Market project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@stockmarket.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('addmoney/', AddMoneyView.as_view(), name='addmoney'),
    path('stocks/', StockListCreateView.as_view(), name='stock-list-create'),
    path('stocks/<int:pk>/', StockDetailView.as_view(), name='stock-detail'),
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('purchasedstocks/', PurchasedStockListCreateView.as_view(), name='purchasedstock-list-create'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
