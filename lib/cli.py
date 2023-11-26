# lib/cli.py
from rich.style import Style
from rich.console import Console
from models.user import User
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
    User.display_all()

def view_user_portfolios():
    user_id = input("Enter user ID: ")
    user = User.find_by_id(user_id)
    if user:
        print(f"\nPortfolios for {user.username}:")
        user.display_portfolios_by_user()
    else:
        print("User not found.")

def create_portfolio():
    user_id = input("Enter user ID: ")
    user = User.find_by_id(user_id)
    if user:
        coin_symbol = input("Enter coin symbol: ")
        amount = float(input("Enter amount: "))
        user.create_portfolio(coin_symbol, amount)
        print(f"Portfolio for {user.username} created successfully.")
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
            print("Portfolio deleted successfully.")
        else:
            print("Portfolio not found.")
    else:
        print("User not found.")

def find_portfolio_by_symbol():
    user_id = input("Enter user ID: ")
    user = User.find_by_id(user_id)
    if user:
        coin_symbol = input("Enter coin symbol: ").upper()
        portfolio = user.find_portfolio_by_symbol(coin_symbol)
        if portfolio:
            print(f"Portfolio found: Portfolio ID: {portfolio.portfolio_id}, Coin: {portfolio.coin_symbol}, Amount: {portfolio.amount}")
        else:
            print("Portfolio not found.")
    else:
        print("User not found.")

def view_all_portfolios():
    User.display_all_portfolios()


if __name__ == "__main__":
    print("")
    console.print(" Welcome to YourCryptoPortfolio! ", style = "dark_green on white bold")
    main()
