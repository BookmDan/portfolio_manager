# CLI Lab

## Learning Goals

- Implement a CLI for an ORM application

---

## Instructions

Run `pipenv install` to create your virtual environment and `pipenv shell` to
enter the virtual environment.

Type in 'python lib/cli.py' to start the main menu. 

<div>
    <a href="https://www.loom.com/embed/b7fe7433847c4251b81ea09a994e1b44?sid=76936476-e243-4425-b3e1-d7147c24e307">
      <p>Command Line Crypto Portfolio - Watch Video</p>
    </a>
</div>

The directory structure is as follows:

```console
.
└── lib
    ├── models
        ├── __init__.py
        ├── cryptocoin.py
        └── portfolio.py
    |   └── user.py
    ├── cli.py
    ├── debug.py
    ├── helpers.py
    ├── portfolio.db
    └── seed.py
├── Pipfile
├── Pipfile.lock
├── portfolio.db
├── pytest.ini
├── README.md
```

### Seeding the database with sample data

The file `lib/seed.py` contains code to initialize the database with sample
departments and employees. Run the following command to seed the database:

```bash
python lib/seed.py
```

You can use the SQLITE EXPLORER extension to explore the initial database
contents. (Another alternative is to run `python lib/debug.py` and use the
`ipbd` session to explore the database)

---

### `cli.py` and `helpers.py`

The file `lib/cli.py` contains a command line interface for our company database
application. The CLI displays a menu of commands. Each numeric choice will call
a function in `lib/helpers.py`. The starter code implements options `0` through
`6`, calling ORM methods related to the `Department` class.

Run `python lib/cli.py` and confirm options 0 through 6 work.

```bash
Please select an option:
1. Create User
2. Display All Users
3. Delete User
4. View User\'s Portfolios
5. Create Portfolio for User
6. Delete Portfolio for User
7. View All Portfolios
8. Find Portfolio by Coin Symbol
9. View All Coin Symbols
Enter x to exit the program
```
