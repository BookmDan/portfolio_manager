# lib/helpers.py
from rich.console import Console
from rich.style import Style
from models import CURSOR, CONN
from models.portfolio import Portfolio
from models.user import User
from models.cryptocoin import CryptoCoin

console = Console()
invalid = Style(color='magenta2', bold=True)

def exit_program():
    console.print("See you next time! (On the moon ^^) ", style="blue3 on grey84 bold")
    console.print('''

                           *     .--.
                                / /  `
               +               | |
                      '         \ \__,
                  *          +   '--'  *
                      +   /\\
         +              .'  '.   *
                *      /======\      +
                      ;:.  _   ;
                      |:. (_)  |
                      |:.  _   |
            +         |:. (_)  |          *
                      ;:.      ;
                    .' \:.    / `.
                   / .-'':._.'`-. \\
                   |/    /||\    \|
             jgs _..--"""````"""--.._
           _.-'``                    ``'-._
         -'                                '-
    ''')
    print('')
    exit()

def add_user():
    print('')
    username = input("Enter username: ")
    try:
        User.create_user(username)
        console.print(f"User '{username}' created successfully", style='green3')
    except Exception as exc:
        print('')
        print("Error creating user: ", exc)

def delete_user_by_id():
    print('')
    users = User.get_all()

    print("Select a user:")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user.username}")

    # try:
    user_name = input("Enter the username of the user: ")
    selected_user = User.find_by_name(user_name)

    #find_by_id method 
    # user_index = int(input("Enter the number of the user: "))
    # selected_user = users[user_index - 1]  # Adjust index since it starts from 1

    if selected_user:
        try: 
            Portfolio.delete_user(selected_user)
            console.print(f"User '{selected_user.username}' deleted successfully", style='red')
        except Exception as exc:
            print('')
            print("Error deleting user: ", exc)
    else:
        print('')
        console.print("User not found.", style='invalid')

    # except (ValueError, IndexError):
    #     print("Invalid input or user not found.")

def user_list():
    return User.display_all()


def view_transactions(user):
    if user:
        transactions = user.get_transactions()
        print('')
        if transactions:
            print(f'Transactions for {user.username}:')
            for i, transaction in enumerate(transactions):
                console.print(i + 1, f"Coin: {transaction['coin_symbol']}, Amount: {transaction['amount']}", style='orange3')
        else:
            console.print(f'No transactions for {user.username}', style='orange3')
        print('')
        input('Press Enter to return to User Details')
    else:
        print("User not found.")


def add_transaction(user):
    print('')
    coin_symbol = input("Enter the symbol of the crypto coin for the new transaction: ").upper()
    amount = float(input("Enter the amount of the crypto coin: "))
    
    crypto_coin = CryptoCoin.find_by_symbol(coin_symbol)
    if crypto_coin:
        try:
            user.create_transaction(coin_symbol, amount)
            print('')
            console.print('Transaction created successfully', style='green3')
        except Exception as exc:
            print('')
            console.print("Error creating transaction: ", exc, style=invalid)
    else: 
        print('')
        console.print(f"Error creating transaction: Coin symbol '{coin_symbol}' not found.", style=invalid)


def remove_transaction(user):
    transactions = user.transactions
    print('')
    if transactions:
        print(f'Transactions for {user.username}:')
        for i, transaction in enumerate(transactions):
            console.print(i + 1, f"Coin: {transaction.crypto_coin.coin_symbol}, Amount: {transaction.amount}", style='orange3')
        print('')
        choice = input("Enter the number for the transaction to delete: ")

        try:
            picked_transaction = transactions[int(choice) - 1]
            print('')
            console.print(f"Delete transaction with Coin: {picked_transaction.crypto_coin.coin_symbol} and Amount: {picked_transaction.amount}?"
                          f" Enter y to confirm, anything else to cancel")
            confirmation = input("> ")
            if confirmation == 'y':
                Transaction.delete_transaction(picked_transaction['transaction_id'])
                print('')
                console.print(f'Transaction deleted', style='green3')
            else:
                print('')
                console.print('Action canceled', style='yellow')
        except (ValueError, IndexError):
            print("")
            console.print("Invalid entry", style=invalid, highlight=False)
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
    
def view_coin_symbols():
    CryptoCoin.display_all()
