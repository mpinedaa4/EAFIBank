class Group():
    def __init__(self):
        self.users = {} #los keys son nombres de usuarios, los values son los montos que han transferido al grupo
        self.capital = 0.0
        self.fidelity = None

    def get_users(self):
        return list(self.users.keys())
    
    def get_capital(self):
        return self.capital
    
    def set_capital(self, new_capital):
        self.capital = new_capital

    def add_user(self, user):
        if len(self.users) == 3:
            return False
        self.users[user.get_name()] = 0

    def add_capital(self, username, new_capital):
        self.capital += new_capital
        self.users[username] += new_capital

    def find_fidelity(self):
        self.fidelity = max(self.users, key=self.users.get)
        return self.fidelity

    def loan(self, user, amount):
        if amount > self.capital:
            print('No hay suficientes fondos para este préstamo.')
            return
        else:
            self.capital -= amount
            if user.get_name() in self.get_users():
                return 0.03
            else:
                return 0.05
    
    def disolve(self):
        total_invested = 0
        for amount in self.users.values():
            total_invested += amount
        for user, money in self.users.items():
            self.users[user] = self.capital * (money/total_invested)
        return self.users



    def __str__(self):
        return f'Miembros -> {self.get_users()} | Capital -> {self.get_capital()}'