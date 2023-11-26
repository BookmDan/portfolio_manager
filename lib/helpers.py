# lib/helpers.py
from rich.console import Console
from rich.style import Style
from models import CURSOR, CONN
from models.portfolio import Portfolio
from models.user import User
from models.transaction import Transaction
from models.cryptocoin import CryptoCoin

console = Console()
invalid = Style(color='magenta2', bold=True)

def exit_program():
    console.print("See you next time! (On the moon ^^) ", style="dark_red on grey84 bold")
    print('')
    exit()

def add_user():
    print('')
    username = input("Enter username: ")
    try:
        User.create(username)
        console.print(f"User '{username}' created successfully", style='green3')
    except Exception as exc:
        print('')
        print("Error creating user: ", exc)

def delete_user_by_id():
    print('')
    user_id = input("Enter ID of the user you want to delete: ")
    user= User.find_by_id(user_id)
    if user:
        try:
            User.delete(user)
            console.print(f"User '{user.username}' deleted successfully", style='green3')
        except Exception as exc:
            print('')
            print("Error deleting user: ", exc)
    else: 
        print('')
        console.print("User not found.", style=invalid)

def user_list():
    return User.display_all()


def view_transactions(user):
    transactions = user.transactions
    print('')
    if transactions:
        print(f'Transactions for {user.username}:')
        for i, transaction in enumerate(transactions):
            console.print(i + 1, f"Coin: {transaction.coin_symbol}, Amount: {transaction.amount}", style='orange3')
    else:
        console.print(f'No transactions for {user.username}', style='orange3')
    print('')
    input('Press Enter to return to User Details')


def add_transaction(user):
    print('')
    coin_symbol = input("Enter the symbol of the crypto coin for the new transaction: ")
    amount = float(input("Enter the amount of the crypto coin: "))
    try:
        user.create_transaction(coin_symbol, amount)
        print('')
        console.print('Transaction created successfully', style='green3')
    except Exception as exc:
        print('')
        console.print("Error creating transaction: ", exc, style=invalid)


def remove_transaction(user):
    transactions = user.transactions
    print('')
    if transactions:
        print(f'Transactions for {user.username}:')
        for i, transaction in enumerate(transactions):
            console.print(i + 1, f"Coin: {transaction.coin_symbol}, Amount: {transaction.amount}", style='orange3')
        print('')
        choice = input("Enter the number for the transaction to delete: ")

        try:
            picked_transaction = transactions[int(choice) - 1]
            print('')
            console.print(f"Delete transaction with Coin: {picked_transaction.coin_symbol} and Amount: {picked_transaction.amount}?"
                          f" Enter y to confirm, anything else to cancel")
            confirmation = input("> ")
            if confirmation == 'y':
                picked_transaction.delete()
                print('')
                console.print(f'Transaction deleted', style='green3')
            else:
                print('')
                console.print('Action canceled', style='yellow')
        except:
            print("")
            console.print(f"Invalid entry: {choice}", style=invalid, highlight=False)
    else:
        console.print(f'No transactions for {user.username}', style='orange3')


def update_user(user):
    print('')
    tmp = user.username
    try:
        username = input('Enter the username for the updated user: ')
        user.username = username
        user.update()
        print('')
        console.print('Update successful', style='green3')
    except Exception as exc:
        user.username = tmp
        console.print("Error updating user: must enter a valid username", style=invalid)

def delete_user(user):
    print('')
    console.print(f'Delete {user.username} and all its transactions? Enter y to confirm, anything else to cancel')
    confirm = input("> ")
    if confirm != 'y':
        print('')
        console.print('Action canceled', style='yellow')
        return 0
    else:
        for transaction in user.transactions:
            transaction.delete()
        user.delete()
        print('')
        console.print('User and transactions deleted', style='green3')
        return 1
    
def create_portfolio():
    user_id = input("Enter user ID: ")
    user = User.find_by_id(user_id)

    if user:
        coin_symbol = input("Enter coin symbol: ")
        amount = float(input("Enter amount: "))

        # Assuming create_portfolio is a method in your User class
        user.create_portfolio(coin_symbol, amount)
        print(f"Portfolio for {user.username} created successfully.")
    else:
        print("User not found.")

def view_coin_symbols():
    CryptoCoin.display_all()
    # coin_symbols = CryptoCoin.display_all()

    # if coin_symbols:
    #     print("All Coin Symbols:")
    #     for symbol in coin_symbols:
    #         print(symbol)
    # else: 
    #     print("No coing symbols found.")
