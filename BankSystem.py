from random import randint
import sqlite3
import os.path

if not os.path.isfile('bank.sqlite'):
    conn = sqlite3.connect('bank.sqlite')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE card(
                        id INTEGER,
                        number TEXT,
                        pin TEXT,
                        balance INTEGER DEFAULT 0
                        );''')
else:
    conn = sqlite3.connect('bank.sqlite')
    cur = conn.cursor()


class Bank:
    LOGIN_MENU_LOOP = False
    _logged_in_number = 0
    _logged_in_balance = 0

    def _create_account(self):
        card_number = self._generate_card_number()
        password = self._generate_pin()
        cur.execute('INSERT INTO card (number, pin) VALUES (?, ?)', (card_number, password))
        conn.commit()
        print('Your card has been created')
        print(f'Your card number:\n{card_number}')
        print(f'Your card PIN:\n{password}\n')

    @staticmethod
    def _generate_pin():
        return f"{randint(0000, 9999):04}"

    @staticmethod
    def _generate_card_number():
        account_identifier = [randint(0, 9) for i in range(9)]
        account_identifier_copy = account_identifier.copy()
        account_identifier_copy = [account_identifier_copy[i] * 2 if i % 2 == 0
                                   else account_identifier_copy[i] for i in range(len(account_identifier_copy))]
        account_identifier_copy = [item - 9 if item > 9 else item for item in account_identifier_copy]
        dig_sum = sum(account_identifier_copy) + 8
        card_number = '400000' + ''.join(map(str, account_identifier))
        for i in range(0, 10):
            if (dig_sum + i) % 10 == 0:
                card_number += str(i)
                break
        return card_number

    def _do_transfer(self):
        pass

    def _balance(self):
        print(f'Balance: {self._logged_in_balance}\n')

    def _add_income(self):
        logged_in_user_income_input = input('Enter income:\n')
        cur.execute('UPDATE card SET balance = balance + ? WHERE number = ?',
                    (logged_in_user_income_input, self._logged_in_number))
        conn.commit()
        self._logged_in_balance += int(logged_in_user_income_input)
        print('Income was added!\n')

    def _close_account(self):
        cur.execute('DELETE FROM card WHERE number = ?', (self._logged_in_number, ))
        conn.commit()
        print('The account has been closed!\n')

    def _login(self):
        user_input_card_number = input('Enter your card number:\n')
        user_input_pin = input('Enter your PIN:\n')
        cur.execute('SELECT number, balance FROM card WHERE number = ? AND pin = ?',
                    (user_input_card_number, user_input_pin))
        logged_in_user_data = cur.fetchone()
        if logged_in_user_data:
            print('You have successfully logged in!\n')
            self.LOGIN_MENU_LOOP = True
            self._logged_in_number, self._logged_in_balance = logged_in_user_data
        else:
            print('Wrong card number or PIN!\n')

    def _login_menu(self):
        self.LOGIN_MENU_LOOP = True
        print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
        user_input = input()
        if user_input == '1':
            self._balance()
        elif user_input == '2':
            self._add_income()
        elif user_input == '3':
            self._do_transfer()
        elif user_input == '4':
            self._close_account()
        elif user_input == '5':
            print('You have successfully logged out!')
            self._logged_in_balance, self._logged_in_number = 0, 0
            self.LOGIN_MENU_LOOP = False
        elif user_input == '0':
            exit()

    def menu(self):
        while True:
            print('1. Create an account\n2. Log into account\n0. Exit')
            user_input = input()
            if user_input == '1':
                self._create_account()
            elif user_input == '2':
                self._login()
                while self.LOGIN_MENU_LOOP:
                    self._login_menu()
            elif user_input == '0':
                exit()


if __name__ == '__main__':
    bank = Bank()
    bank.menu()
