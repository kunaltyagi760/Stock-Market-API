# Stock Market API

The Stock Market API is a Django-based RESTful API that allows users to buy and sell stocks, view purchased stocks, manage transactions, and add money to their accounts. The API is designed to handle user authentication and authorization using JWT (JSON Web Tokens) and provides endpoints for stock management, transactions, and user registration/login.

## Features

- **User Registration & Authentication**: Securely register and log in users using JWT-based authentication.
- **Stock Management**: Add, update, view, and delete stock information.
- **Transaction Management**: Track and manage stock purchases and related transactions.
- **Account Management**: Add money to user accounts for transactions.
- **Bearer Token Security**: Secure API endpoints with Bearer token authentication.

## Endpoints

### Authentication

- **POST** `/login/`: Authenticates a user and returns access and refresh tokens.
- **POST** `/register/`: Registers a new user.
- **POST** `/token/refresh/`: Refreshes the access token using the refresh token.

### Stocks

- **GET** `/stocks/`: List all available stocks.
- **POST** `/stocks/`: Create a new stock.
- **GET** `/stocks/{id}/`: Retrieve details of a specific stock.
- **PUT** `/stocks/{id}/`: Update details of a specific stock.
- **DELETE** `/stocks/{id}/`: Delete a specific stock.

### Transactions

- **GET** `/transactions/`: List all transactions.
- **POST** `/transactions/`: Create a new transaction.
- **GET** `/transactions/{id}/`: Retrieve details of a specific transaction.

### Purchased Stocks

- **GET** `/purchasedstocks/`: List all purchased stocks.

### Account Management

- **GET** `/addmoney/`: View the amount of money in a user's account.
- **PUT** `/addmoney/`: Add money to a user's account.

## Security

All endpoints (except for registration and login) are secured with JWT-based Bearer token authentication. You must include the following header in your requests to access these endpoints:

```http
Authorization: Bearer <your-token>
```

## Swagger Documentation
To explore the API, you can use the Swagger UI provided by the project. It allows you to test the endpoints directly from the browser.

```http
URL: http://127.0.0.1:8000/stockapp/swagger/
```

## Setup Instructions
### Clone the Repository:

```bash
git clone <repository-url>
cd stock-market-api
```
### Install Dependencies:

```python
pip install -r requirements.txt
```
### Apply Migrations:

```python
python manage.py makemigrations
python manage.py migrate
```
### Run the Server:

```python
python manage.py runserver
```
### Access Swagger Documentation:

Open your browser and go to

```http
URL: http://127.0.0.1:8000/stockapp/swagger/
```

