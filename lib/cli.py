# lib/cli.py
from rich.style import Style
from rich.console import Console
from models.user import User
from models.portfolio import Portfolio

from helpers import exit_program, add_user, delete_user_by_id

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
        elif choice.lower() == 'x':
            exit_program()
        else:
            print("Invalid choice. Please enter a number from 1 to 10.")

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
    print("Enter x to exit the program")

def display_all_users():
    print("All Users:")
    users = User.get_all()
    for i, user in enumerate(users):
         print(f"User ID: {i + 1}, Username: {user.username}")

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
    users = User.get_all()

    print("Select a user:")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user.username}")

    try:
        user_index = int(input("Enter the number of the user: "))
        selected_user = users[user_index - 1]  # Adjust index since it starts from 1

        if selected_user:
            coin_symbol = input("Enter coin symbol: ").upper()
            amount = float(input("Enter amount: "))
            
            try:
                Portfolio.create_portfolio(selected_user, coin_symbol, amount)
                console.print(f"Portfolio for {selected_user.username} created successfully.", style='green3')
            except Exception as exc:
                print('')
                print("Error creating portfolio: ", exc)
        else:
            print("User not found.")
    except (ValueError, IndexError):
        print("Invalid input or user not found.")


        
def delete_portfolio():
    users = User.get_all()

    print("Select a user:")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user.username}")

    try:
        user_index = int(input("Enter the number of the user: "))
        selected_user = users[user_index - 1]  # Adjust index since it starts from 1

        if selected_user:
            portfolio_id = input("Enter portfolio ID: ")
            portfolio = selected_user.find_portfolio_by_id(portfolio_id)
            
            if portfolio:
                try:
                    Portfolio.delete_portfolio(portfolio)
                    console.print(f"Portfolio deleted successfully.", style='red')
                except Exception as exc:
                    print('')
                    print("Error deleting portfolio: ", exc)
            else:
                console.print("Portfolio not found.", style='red')
        else:
            print("User not found.")
    except (ValueError, IndexError):
        print("Invalid input or user not found.")


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
                print(f"  Portfolio ID: {portfolio.get('id')}, Coin Symbol: {portfolio.get('coin_symbol', 'N/A')}, Amount: {portfolio.get('amount')}")

        else:
            console.print("No portfolios found.")


if __name__ == "__main__":
    print("")
    console.print(" Welcome to Portfolio Manager! ", style = "dark_green on white bold")
    main()
