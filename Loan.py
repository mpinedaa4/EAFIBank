class Loan:
    def __init__(self, amount, interest, months):
        self.interest_rate = interest
        self.months = months
        self.amount = amount

    def get_amount(self):
        return self.amount

    def amount_to_pay(self, months):
        if months > self.months:
            print('Número de meses inválido.')
            return
        amount_per_month = (self.amount/self.months) + ((self.amount/self.months) * self.interest_rate)
        self.amount = amount_per_month * self.months
        amount = amount_per_month * months
        print (f'Monto a pagar: ${amount}')
        return amount
    
    def pay(self, amount, months):
        self.amount -= amount
        self.months -= months

    def __str__(self):
        return f'Monto: ${self.amount} | Tasa de interés: {self.interest_rate * 100}% | Meses: {self.months}'