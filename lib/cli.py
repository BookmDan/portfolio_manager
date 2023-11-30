# lib/cli.py
from rich.style import Style
from rich.console import Console
from models.user import User
from models.portfolio import Portfolio

from helpers import exit_program, add_user, view_coin_symbols, delete_user_by_id

console = Console()

def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "1":
            add_user()
        elif choice == "2":
            display_all_users()
        elif choice == "3":
            delete_user_by_id()
        elif choice == "4":
            view_user_portfolios()
        elif choice == "5":
            create_portfolio()
        elif choice == "6":
            delete_portfolio()
        elif choice == "7":
            view_all_portfolios()
        elif choice == "8":
            find_portfolio_by_symbol()
        elif choice == "9":
            view_coin_symbols()
        elif choice.lower() == 'x':
            exit_program()
        else:
            print("Invalid choice")

def menu():
    print('')
    console.print("------[blue]Main Menu[/blue]-----------------", style="dark_sea_green bold")
    print(" ")

    print("1. Create User")
    print("2. Display All Users")
    print("3. Delete User")
    print("4. View User's Portfolios")
    print("5. Create Portfolio for User")
    print("6. Delete Portfolio for User")
    print("7. View All Portfolios")
    print("8. Find Portfolio by Coin Symbol")
    print("9. View All Coin Symbols")
    # console.print(f"7. View All Coin Symbols ", style='green3')
    print("Enter x to exit the program")

def display_all_users():
    print("All Users:")
    users = User.get_all()
    for i, user in enumerate(users):
         print(f"User ID: {i + 1}, Username: {user.username}")

# def view_user_portfolios():
#     user_id = input("Enter user ID: ")
#     user = User.find_by_id(user_id)
#     if user:
#         print(f"\nPortfolios for {user.username}:")
#         Portfolio.display_portfolios_by_user(int(user_id))
#     else:
#         print("User not found.")

def view_user_portfolios():
    users = User.get_all()

    print("Select a user:")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user.username}")

    try:
        user_index = int(input("Enter the number of the user: "))
        selected_user = users[user_index - 1]  # Adjust index since it starts from 1
        user_id = selected_user.user_id

        print(f"\nPortfolios for {selected_user.username}:")
        Portfolio.display_portfolios_by_user(user_id)
    except (ValueError, IndexError):
        print("Invalid input or user not found.")

def create_portfolio():
    user_id = input("Enter user ID: ")
    user = User.find_by_id(user_id)
    if user:
        coin_symbol = input("Enter coin symbol: ").upper()
        amount = float(input("Enter amount: "))
        Portfolio.create_portfolio(user, coin_symbol, amount)
        console.print(f"Portfolio for {user.username} created successfully.", style='green3')
    else:
        print("User not found.")

def create_portfolio():
    user_id = input("Enter user ID: ")
    user = User.find_by_id(user_id)
    if user:
        coin_symbol = input("Enter coin symbol: ").upper()
        amount = float(input("Enter amount: "))
        user.create_portfolio(coin_symbol, amount)
        console.print(f"Portfolio for {user.username} created successfully.", style='green3')
    else:
        print("User not found.")

def delete_portfolio():
    user_id = input("Enter user ID: ")
    user_instance = User.find_by_id(user_id)
    if user_instance:
        portfolio_id = input("Enter portfolio ID: ")
        portfolio = user_instance.find_portfolio_by_id(portfolio_id)
        if portfolio:
            user_instance.delete_portfolio(portfolio)
            console.print(f"Portfolio deleted successfully.", style='red')
        else:
            console.print("Portfolio not found.", style='red')
    else:
        print("User not found.")

# def find_portfolio_by_symbol():
#     user_id = input("Enter user ID: ")
    
#     user = User.find_by_id(user_id)
#     if user:
#         coin_symbol = input("Enter coin symbol: ").upper()
#         portfolio = user.find_portfolio_by_symbol(user_id, coin_symbol)
#         if portfolio:
#             print(f"Portfolio found: Portfolio ID: {portfolio.portfolio_id}, CryptoCoin ID: {portfolio.coin_symbol}, Amount: {portfolio.amount}")
#         # else:
#         #     print("Portfolio not found.")
#     else:
#         print("User not found.")

def find_portfolio_by_symbol():
    users = User.get_all()

    print("Select a user:")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user.username}")

    try:
        user_index = int(input("Enter the number of the user: "))
        selected_user = users[user_index - 1]  # Adjust index since it starts from 1
        user_id = selected_user.user_id

        print(f"\nFind portfolio for {selected_user.username}:")
        coin_symbol = input("Enter coin symbol: ").upper()

        Portfolio.find_portfolio_by_symbol(user_id, coin_symbol)
    except (ValueError, IndexError):
        print("Invalid input or user not found.")


def display_all_users():
    print("All Users:")
    users = User.get_all()
    for i, user in enumerate(users):
         print(f"User ID: {i + 1}, Username: {user.username}")

def view_all_portfolios():
    # User.display_all_portfolios()
    users = User.get_all()
    for i, user in enumerate(users):
        portfolios = Portfolio.display_all_portfolios(user)
        print(f"User ID: {i + 1}, Username: {user.username}")
        # print(f"User ID: {user.user_id}, Username: {user.username}")
        if portfolios:
            for portfolio in portfolios:
                print(f"  Portfolio ID: {portfolio['portfolio_id']}, Coin ID: {portfolio['coin_id']}, Amount: {portfolio['amount']}")
        else:
            print("  No portfolios found.")


if __name__ == "__main__":
    print("")
    console.print(" Welcome to YourCryptoPortfolio! ", style = "dark_green on white bold")
    main()
