# lib/cli.py

from helpers import (
    exit_program,
    helper_1
)
from models.crypto_model import CryptoCoin, Portfolio  # Import new models
from services.coin_gecko_api import CoinGeckoAPI  # Import CoinGecko API

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
        else:
            print("Invalid choice")

def crypto_menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Some useful function")
    print("2. View Portfolio")

def view_portfolio():
    # Logic to retrieve and display user's cryptocurrency portfolio
    # You can interact with the CryptoCoin and Portfolio models and use the CoinGecko API
    pass

if __name__ == "__main__":
    main()
