import os

class Menu():
    def login(self):
        print('¡Bienvenido a EAFIBank!')
        print('Por favor elige una opción:')
        print('1. Iniciar sesión')
        print('2. Crear usuario')
        try:
            ans = int(input('Ingresa tu respuesta: '))
            return ans
        except:
            pass
        
    def main_menu(self):
        print(':::: Menú Principal ::::')
        print('1. Crear un grupo de ahorro')
        print('2. Invitar usuarios a un grupo de ahorro')
        print('3. Agregar capital a un grupo de ahorro')
        print('4. Solicitar préstamo')
        print('5. Pagar préstamo')
        print('6. Consignar a cuenta de ahorros')
        print('7. Disolver un grupo')
        print('8. Ver historial de transacciones')
        print('9. Finalizar sesión')
        try:
            ans = int(input('Ingresa tu respuesta: '))
            return ans
        except:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('No has ingresado una respuesta válida, por favor inténtalo nuevamente.')
            print('='*30)