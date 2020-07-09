from random import randint
import sqlite3

conn = sqlite3.connect('bank.sqlite')
cur = conn.cursor()


class Bank:
    LOGIN_MENU_LOOP = False

    def __create_account(self):
        card_number = self.__generate_card_number()
        password = self.__generate_pin()
        cur.execute('INSERT INTO card (number, pin) VALUES (?, ?)', (card_number, password))
        conn.commit()
        print('Your card has been created')
        print(f'Your card number:\n{card_number}')
        print(f'Your card PIN:\n{password}\n')

    @staticmethod
    def __generate_pin():
        return f"{randint(0000, 9999):04}"

    @staticmethod
    def __generate_card_number():
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

    def login(self):
        cur.execute('SELECT number, pin FROM card')
        print('Enter your card number:')
        user_input_card_number = input()
        print('Enter your PIN:')
        user_input_pin = input()
        for card_number, pin in cur.fetchall():
            if user_input_card_number == card_number and user_input_pin == pin:
                print('You have successfully logged in!\n')
                self.LOGIN_MENU_LOOP = True
                break
        else:
            print('Wrong card number or PIN!\n')

    def __login_menu(self):
        self.LOGIN_MENU_LOOP = True
        print('1. Balance\n2. Log out\n0. Exit')
        user_input = input()
        if user_input == '1':
            print('Balance: 0\n')
        elif user_input == '2':
            print('You have successfully logged out!')
            self.LOGIN_MENU_LOOP = False
        elif user_input == '0':
            exit()

    def menu(self):
        while True:
            print('1. Create an account\n2. Log into account\n0. Exit')
            user_input = input()
            if user_input == '1':
                self.__create_account()
            elif user_input == '2':
                self.login()
                while self.LOGIN_MENU_LOOP:
                    self.__login_menu()
            elif user_input == '0':
                exit()


if __name__ == '__main__':
    bank = Bank()
    bank.menu()
