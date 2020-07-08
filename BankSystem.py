from random import randint
import sqlite3

conn = sqlite3.connect('bank.sqlite')
cur = conn.cursor()


MAIN_MENU_LOOP = True
LOGIN_MENU_LOOP = False


def create_account():
    card_number = generate_card_number()
    password = generate_password()
    cur.execute('INSERT INTO card (number, pin) VALUES (?, ?)', (card_number, password))
    conn.commit()
    print('Your card has been created')
    print(f'Your card number:\n{card_number}')
    print(f'Your card PIN:\n{password}\n')


def generate_password():
    return f"{randint(0000, 9999):04}"


def generate_card_number():
    BIN = '400000'
    account_identifier = []
    check_sum = 0
    for i in range(0, 9):
        account_identifier.append(randint(0, 9))
    account_identifier_copy = account_identifier.copy()
    for i in range(0, 9, 2):
        account_identifier_copy[i] *= 2
    for i in range(0, 9):
        if account_identifier_copy[i] > 9:
            account_identifier_copy[i] -= 9
    dig_sum = sum(account_identifier_copy) + 8
    for i in range(0, 10):
        if (dig_sum + i) % 10 == 0:
            check_sum += i
            break
    card_number = BIN + ''.join(map(str, account_identifier)) + str(check_sum)
    return card_number


def login():
    global LOGIN_MENU_LOOP
    cur.execute('SELECT number, pin FROM card')
    print('Enter your card number:')
    user_input_card_number = input()
    print('Enter your PIN:')
    user_input_password = input()
    for card_number, password in cur.fetchall():
        if user_input_card_number == card_number and user_input_password == password:
            print('You have successfully logged in!\n')
            LOGIN_MENU_LOOP = True
            break
    else:
        print('Wrong card number or PIN!\n')


def login_menu():
    global LOGIN_MENU_LOOP, MAIN_MENU_LOOP
    print('1. Balance\n2. Log out\n0. Exit')
    user_input = input()
    if user_input == '1':
        print('Balance: 0\n')
    elif user_input == '2':
        print('You have successfully logged out!')
        LOGIN_MENU_LOOP = False
    elif user_input == '0':
        LOGIN_MENU_LOOP = False
        MAIN_MENU_LOOP = False


def menu():
    global MAIN_MENU_LOOP
    print('1. Create an account\n2. Log into account\n0. Exit')
    user_input = input()
    if user_input == '1':
        create_account()
    elif user_input == '2':
        login()
        while LOGIN_MENU_LOOP:
            login_menu()
    elif user_input == '0':
        MAIN_MENU_LOOP = False


if __name__ == '__main__':
    while MAIN_MENU_LOOP:
        menu()
