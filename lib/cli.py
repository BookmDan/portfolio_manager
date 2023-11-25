# lib/cli.py
from rich.style import Style
from rich.console import Console
from helpers import exit_program
console = Console()

def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            create_user()
        elif choice == "2":
            display_all_users()
        elif choice == "3":
            view_user_portfolios()
        elif choice == "4":
            create_portfolio()
        elif choice == "5":
            delete_portfolio()
        elif choice == "6":
            find_portfolio_by_symbol()
        else:
            print("Invalid choice")

def menu():
    print('')
    console.print("------[blue]Main Menu[/blue]-----------------", style="dark_sea_green bold")
    print(" ")
    
    print("1. Create User")
    print("2. Display All Users")
    print("3. View User's Portfolios")
    print("4. Create Portfolio for User")
    print("5. Delete Portfolio for User")
    print("6. Find Portfolio by Coin Symbol")
    print("Enter x to exit the program")

def create_user():
    username = input("Enter username: ")
    User.create(username)
    print(f"User {username} created successfully.")

def display_all_users():
    print("All Users:")
    User.display_all()

def view_user_portfolios():
    user_id = input("Enter user ID: ")
    user = User.find_by_id(user_id)
    if user:
        print(f"\nPortfolios for {user.username}:")
        user.display_all_portfolios()
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
    user = User.find_by_id(user_id)
    if user:
        portfolio_id = input("Enter portfolio ID: ")
        portfolio = user.find_portfolio_by_id(portfolio_id)
        if portfolio:
            user.delete_portfolio(portfolio)
            print("Portfolio deleted successfully.")
        else:
            print("Portfolio not found.")
    else:
        print("User not found.")

def find_portfolio_by_symbol():
    user_id = input("Enter user ID: ")
    user = User.find_by_id(user_id)
    if user:
        coin_symbol = input("Enter coin symbol: ")
        portfolio = user.find_portfolio_by_symbol(coin_symbol)
        if portfolio:
            print(f"Portfolio found: Portfolio ID: {portfolio.portfolio_id}, Coin: {portfolio.coin_symbol}, Amount: {portfolio.amount}")
        else:
            print("Portfolio not found.")
    else:
        print("User not found.")

if __name__ == "__main__":
    print("")
    console.print(" Welcome to YourCryptoPortfolio! ", style = "dark_green on white bold")
    print("")
    main()
    main()
