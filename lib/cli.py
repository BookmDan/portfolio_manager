# lib/cli.py

from helpers import exit_program
from models.crypto_model import CryptoCoin, Portfolio
from services.coin_gecko_api import CoinGeckoAPI

def main():
    while True:
        crypto_menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            helper_1()
        elif choice == "2":
            view_portfolio()
        elif choice == "3":
            search_crypto_price()
        elif choice == "4":
            buy_crypto()
        elif choice == "5":
            sell_crypto()
        else:
            print("Invalid choice")

def crypto_menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Some useful function")
    print("2. View Portfolio")
    print("3. Search Crypto Price")
    print("4. Buy Crypto")
    print("5. Sell Crypto")

def buy_crypto():
    coin_id = input("Enter the crypto ID to buy: ")
    amount = float(input("Enter the amount to buy: "))
    
    # Get current price
    current_price = CoinGeckoAPI.get_crypto_price(coin_id)

    # Calculate total cost
    total_cost = amount * current_price

    # Check if the user has enough funds
    # For simplicity, assuming user has enough funds for now
    # In a real-world scenario, you'd check the user's balance before proceeding

    # Create a new transaction
    transaction = Portfolio(coin_id=coin_id, amount=amount, transaction_type='buy', cost=total_cost)
    
    # Update the portfolio
    update_portfolio(transaction)

def sell_crypto():
    coin_id = input("Enter the crypto ID to sell: ")
    amount = float(input("Enter the amount to sell: "))
    
    # Get current price
    current_price = CoinGeckoAPI.get_crypto_price(coin_id)

    # Calculate total sale amount
    total_sale_amount = amount * current_price

    # Check if the user has enough coins to sell
    # For simplicity, assuming user has enough coins for now
    # In a real-world scenario, you'd check the user's coin balance before proceeding

    # Create a new transaction
    transaction = Portfolio(coin_id=coin_id, amount=-amount, transaction_type='sell', cost=total_sale_amount)
    
    # Update the portfolio
    update_portfolio(transaction)

def update_portfolio(transaction):
    # Logic to update the user's portfolio based on the transaction
    # For simplicity, assuming that user_id is 1 for now
    user_id = 1
    
    # Retrieve the user's portfolio
    user_portfolio = Portfolio.query.filter_by(user_id=user_id, coin_id=transaction.coin_id).first()

    if user_portfolio:
        # Update existing entry
        user_portfolio.amount += transaction.amount
        user_portfolio.cost += transaction.cost
    else:
        # Create a new entry in the portfolio
        user_portfolio = Portfolio(user_id=user_id, coin_id=transaction.coin_id,
                                   amount=transaction.amount, cost=transaction.cost)
        db.session.add(user_portfolio)

    # Commit the changes
    db.session.commit()
