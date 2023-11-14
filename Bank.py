class Bank():
    def __init__(self):
        self.users = []
        self.funds = 0.0
        self.groups = []
        self.fidelity = []
    
    def get_users(self):
        return self.users
    
    def add_user(self, user):
        self.users.append(user)

    def get_by_username(self, username):
        for user in self.users:
            if username == user.get_name():
                return user
            
    def find_users(self, user):
        users = []
        for group in user.get_groups():
            users += list(filter(lambda x: x not in users, list(filter(lambda x: x in group.get_users(), group.get_users()))))
        return users
    
    def fill_groups(self):
        for user in self.get_users():
            for group in user.get_groups():
                if group not in self.groups:
                    self.groups.append(group)
        
        self.fidelity = [x.find_fidelity() for x in self.groups]

    def find_groups(self, target):
        self.fill_groups()
        usernames = self.find_users(target)
        groups = []
        for username in usernames:
            for user in self.users:
                if username == user.get_name():
                    groups += list(filter(lambda x: x not in groups, list(filter(lambda x: x in user.get_groups(), user.get_groups()))))
        return groups
    
    def disolve_group(self, group):
        self.fill_groups()
        self.groups.remove(group)

    def comission(self, capital):
        self.funds += (capital * 0.001)
        print(f'El banco ha cobrado una comisión de ${capital * 0.001}')
        capital -= (capital * 0.001)
        return capital
    
    def loan_comission(self, user, capital):
        if user.get_name() in self.fidelity:
            self.funds += (capital * 0.00099)
            print(f'El banco ha cobrado una comisión de ${capital * 0.00099}')
            capital -= (capital * 0.00099)
            return capital
        else:
            self.funds += (capital * 0.001)
            print(f'El banco ha cobrado una comisión de ${capital * 0.001}')
            capital -= (capital * 0.001)
            return capital
    
    def pay_comission(self, user, capital):
        if user.get_name() in self.fidelity:
            self.funds += (capital * 0.00099)
            print(f'El banco ha cobrado una comisión de ${capital * 0.00099}')
            capital += (capital * 0.00099)
            return capital
        else:
            self.funds += (capital * 0.001)
            print(f'El banco ha cobrado una comisión de ${capital * 0.001}')
            capital += (capital * 0.001)
            return capital
        
    def disolve_comission(self, capital):
        self.funds += (capital * 0.05)
        print(f'El banco ha cobrado una comisión de ${capital * 0.05}')
        capital -= (capital * 0.05)
        return capital