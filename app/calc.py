def add(num1: int, num2: int):
    return num1 + num2

def sub(num1: int, num2: int):
    return num1 - num2

def mul(num1: int, num2: int):
    return num1 * num2

def div(num1: int, num2: int):
    return num1 / num2

# New exception as if code break due to some other exception it test won't pass
class InsufficientFund(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFund("Insufficient Fund")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1