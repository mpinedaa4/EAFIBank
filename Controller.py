from Menu import *
from Bank import *
from User import *
from Group import *
from Loan import *
import pickle
import sys
import os

class Controller():
    def __init__(self):
        self.menu = Menu()
        self.bank = Bank()
        self.actual_user = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def validate_username(self, username):
        for user in self.bank.get_users():
            if username == user.get_name():
                return True
        return False
    
    def validate_password(self, username, password):
        for user in self.bank.get_users():
            if username == user.get_name():
                if password == user.get_password():
                    self.actual_user = user
                    return True
        return False

    def start(self):
        try:
            with open('serialized.pkl', 'rb') as file:
                self.bank = pickle.load(file)
        except:
            pass
        while True:
            ans = self.menu.login()
            if ans == 1:
                name = input('Ingresa tu nombre de usuario: ')
                if self.validate_username(name):
                    password = input('Ingresa tu contraseña: ')
                    if self.validate_password(name, password):
                        self.actual_user = self.bank.get_by_username(name)
                        self.clear_screen()
                        return True
                    else:
                        self.clear_screen()
                        print('La contraseña es incorrecta, inténtalo nuevamente.')
                        print('='*30)
                else:
                    self.clear_screen()
                    print('El usuario no existe.')
                    print('='*30)

            elif ans == 2:
                name = input('Ingresa un nombre de usuario: ')
                if not self.validate_username(name):
                    password = input('Ingresa una contraseña: ')
                    self.actual_user = User(name, password)
                    self.bank.add_user(self.actual_user)
                    self.clear_screen()
                    return True
                self.clear_screen()
                print('El nombre de usuario no está disponible, inténtalo nuevamente.')
                print('='*30)
            else:
                self.clear_screen()
                print('No has ingresado una opción válida, por favor inténtalo nuevamente.')
                print('='*30)
                continue


    def main_stream(self):
        ans = self.menu.main_menu()
        if ans == 1:
            new_group = Group()
            if self.actual_user.add_group(new_group):
                new_group.add_user(self.actual_user)
                self.clear_screen()
                print('Se ha creado el grupo con éxito.')
                print('='*30)

        elif ans == 2:
            self.clear_screen()
            if self.actual_user.show_groups() == False:
                return
            try:
                name = input('Ingresa el nombre del usuario que deseas agregar: ')
                if self.validate_username(name):
                    index = int(input('Ingresa el número del grupo al que deseas agregar un usuario: '))
                    try:
                        user = self.bank.get_by_username(name)
                        if name in self.actual_user.get_groups()[index-1].get_users():
                            self.clear_screen()
                            print('El usuario ya se encuentra en ese grupo.')
                            print('='*30)
                            return
                        if self.actual_user.get_groups()[index-1].add_user(user) == False:
                            self.clear_screen()
                            print('No puedes agregar un nuevo usuario porque ya hay tres usuarios en este grupo.')
                            print('='*30)
                            return
                        if user.add_group(self.actual_user.get_groups()[index-1]) == False:
                            return
                        self.clear_screen()
                        print('Se ha agregado exitosamente al usuario.')
                        print('='*30)
                    except:
                        self.clear_screen()
                        print('No has ingresado un grupo válido.')
                        print('='*30)
                else:
                    self.clear_screen()
                    print('No has ingresado un usuario válido.')
                    print('='*30)
            except:
                self.clear_screen()
                print('No has ingresado un valor válido.')
                print('='*30)

        elif ans == 3:
            self.clear_screen()
            self.actual_user.show_groups()
            try:
                index = int(input('Ingresa el número del grupo al que deseas agregar capital: '))
                print(f'Tu saldo actual es ${self.actual_user.get_money()}')
                capital = float(input('Ingresa el monto que deseas transferir al grupo de ahorro: '))
            except:
                self.clear_screen()
                print('No has ingresado un valor válido.')
                print('='*30)
                return
            if capital > self.actual_user.get_money():
                self.clear_screen()
                print('No tienes suficientes fondos')
                print('='*30)
                return
            else:
                try:
                    group = self.actual_user.get_groups()[index-1]
                    self.actual_user.add_transaction('Transferencia a grupo de ahorro', capital)
                    capital = self.bank.comission(capital)
                    group.add_capital(self.actual_user.get_name(), capital)
                    print('='*30)
                except:
                    self.clear_screen()
                    print('No has ingresado un valor válido.')
                    print('='*30)
            

        elif ans == 4:
            self.clear_screen()
            groups = self.bank.find_groups(self.actual_user)
            if len(groups) == 0:
                self.clear_screen()
                print('Actualmente no hay disponible ningún grupo al que puedas pedir un préstamo.')
                print('='*30)
            else:
                index = 1
                for group in groups:
                    print(f'Grupo {index}: {group}')
                    index += 1
                try:
                    max_loan = self.actual_user.total_invested()
                    if max_loan == 0:
                        self.clear_screen()
                        print('No puedes pedir prestado porque no has depositado dinero en ningún grupo.')
                        print('='*30)
                        return
                    index = int(input('Ingresa el número del grupo del cual deseas pedir un préstamo: '))
                    amount = int(input(f'El monto máximo que puedes prestar es ${max_loan}. Ingresa el monto que deseas prestar: '))
                except:
                    self.clear_screen()
                    print('No has ingresado un valor válido.')
                    print('='*30)
                    return
                if amount > max_loan:
                    self.clear_screen()
                    print('El monto que deseas prestar supera el monto máximo.')
                    print('='*30)
                    return
                try:
                    interest = groups[index-1].loan(self.actual_user, amount)
                except:
                    self.clear_screen()
                    print('No has ingresado un valor válido.')
                    print('='*30)
                    return
                if interest == None:
                    print('='*30)
                    return
                try:
                    months = int(input('Ingrese el número de meses para pagar (2 o más): '))
                except:
                    print('Ingreaste un valor inválido.')
                if months < 2:
                    self.clear_screen()
                    print('Ingresaste un plazo inadecuado.')
                    print('='*30)
                    return
                loan = Loan(amount, interest, months)
                amount = self.bank.loan_comission(self.actual_user, amount)
                print('='*30)
                self.actual_user.add_loan(loan)
                self.actual_user.add_transaction('Préstamo grupo de ahorro', amount)

        elif ans == 5:
            self.clear_screen()
            print('Tienes los siguiente préstamos:')
            if self.actual_user.show_loans() == False:
                return
            try:
                index = int(input('Selecciona el número del préstamo que deseas pagar: '))
                loan = self.actual_user.get_loans()[index-1]
                months = int(input('Selecciona el número de meses que deseas pagar: '))
                amount = loan.amount_to_pay(months)
                choice = input('¿Deseas realizar el pago? (S/N): ')
                if choice.lower() == 's':
                    amount = self.bank.pay_comission(self.actual_user, amount)
                    if amount > self.actual_user.get_money():
                        self.clear_screen()
                        print('No tienes suficiente saldo para pagar. La comisión del banco ha sido devuelta a tu cuenta de ahorros.')
                        print('='*30)
                        return
                    self.actual_user.pay_loan(loan, amount)
                    loan.pay(amount, months)
                elif choice.lower() == 'n':
                    self.clear_screen()
                    print('No se ha realizado el pago.')
                    print('='*30)
                    return
                else:
                    self.clear_screen()
                    print('No has ingresado un valor válido.')
                    print('='*30)
            except:
                self.clear_screen()
                print('No has ingresado un valor válido.')
                print('='*30)

        elif ans == 6:
            self.clear_screen()
            try:
                amount = int(input('Ingresa el monto que deseas consignar: '))
                amount = self.bank.comission(amount)
                self.actual_user.add_money(amount)
                print(f'Se ha consignado ${amount} a tu cuenta de ahorros. \nTu nuevo saldo es ${self.actual_user.get_money()}.')
                print('='*30)
                self.actual_user.add_transaction('Consignación a cuenta de ahorros', amount)
            except:
                self.clear_screen()
                print('No has ingresado un valor válido.')
                print('='*30)

        elif ans == 7:
            self.clear_screen()
            self.actual_user.show_groups()
            try:
                index = int(input('Ingresa el número del grupo que deseas disolver: '))
                group = self.actual_user.get_groups()[index-1]
            except:
                self.clear_screen()
                print('No has ingresado un valor válido.')
                print('='*30)
                return
            capital = self.bank.disolve_comission(group.get_capital())
            group.set_capital(capital)
            self.bank.disolve_group(group)
            user_dict = group.disolve()
            for username, money in user_dict.items():
                user = self.bank.get_by_username(username)
                user.add_money(money)
                print(f'Se ha transferido ${money} a la cuenta de {user.get_name()}. El nuevo saldo es ${user.get_money()}.')
                user.disolve_group(group)
            print('='*30)
            

        elif ans == 8:
            self.clear_screen()
            self.actual_user.show_transactions()

        elif ans == 9:
            self.clear_screen()
            serialized = self.bank
            with open('serialized.pkl', 'wb') as file:
                pickle.dump(serialized, file)
            print('Has finalizado sesión con éxito.')
            sys.exit(0)

        else:
            self.clear_screen()
            print('No has ingresado una opción válida, por favor inténtalo nuevamente.')
            print('='*30)
            return True