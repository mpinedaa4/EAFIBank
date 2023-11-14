import time
from datetime import date

class User():
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.money = 100.0
        self.transactions = []
        self.groups = []
        self.loans = []
    
    def get_name(self):
        return self.name
    
    def get_password(self):
        return self.password
    
    def get_money(self):
        return self.money
    
    def get_groups(self):
        return self.groups
    
    def get_loans(self):
        return self.loans
    
    def add_money(self, money):
        self.money += money

    def reduce_money(self, money):
        self.money -= money
    
    def add_group(self, group):
        if len(self.groups) == 3:
            print('No fue posible porque ya está afiliado a tres grupos.')
            print('='*30)
            return False
        self.groups.append(group)
        return True

    def show_groups(self):
        if len(self.groups) == 0:
            print('No haces parte de ningún grupo')
            print('='*30)
            return False
        else:
            print('Haces parte de los siguientes grupos:')
            index = 1
            for group in self.groups:
                print(f'Grupo {index}: {group}')
                index += 1

    def disolve_group(self, group):
        self.groups.remove(group)

    def add_loan(self, loan):
        self.loans.append(loan)

    def pay_loan(self, loan, amount):
        self.money -= amount
        if loan in self.loans:
            if loan.get_amount() - amount <= 0:
                self.loans.remove(loan)
            print('El pago se ha realizado exitosamente.')
            print('='*30)

    def show_loans(self):
        if len(self.loans) == 0:
            print('No tienes préstamos actualmente.')
            print('='*30)
            return False
        index = 1
        for loan in self.loans:
            print(f'{index}. {loan}')
            index += 1

    def add_transaction(self, type, capital):
        current_date = date.today()
        current_time = time.strftime("%H:%M:%S")
        current_money = self.money
        transaction_type = type
        value = capital
        if type == 'Préstamo grupo de ahorro':
            new_money = self.money + capital
        elif type == 'Consignación a cuenta de ahorros':
            new_money = self.money
        else:
            new_money = self.money - capital
        self.money = new_money
        transaction = (current_date, current_time, current_money, transaction_type, value, new_money)
        self.transactions.append(transaction)

    def show_transactions(self):
        if len(self.transactions) == 0:
            print('No has realizado transacciones aún.')
            return
        print ('Historial de transacciones: ')
        index = 1
        for transaction in self.transactions:
            print(f'{index}. Fecha: {transaction[0]} | Hora: {transaction[1]} | Tipo de transacción: {transaction[3]} | Saldo inicial: ${transaction[2]} | Valor de la transacción: ${transaction[4]} | Saldo final: ${transaction[5]}')
            index += 1
        print('='*30)

    def total_invested(self):
        total = 0
        for transaction in self.transactions:
            if transaction[3] == 'Transferencia a grupo de ahorro':
                total += transaction[4]
        return total