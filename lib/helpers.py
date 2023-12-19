# lib/helpers.py
from rich.console import Console
from rich.style import Style
from models import CURSOR, CONN
from models.portfolio import Portfolio
from models.user import User

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
