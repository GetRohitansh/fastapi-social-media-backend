from app.calc import add, sub, mul, div, BankAccount, InsufficientFund
import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [(10,12,22), (11,22,33)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

def test_sub():
    assert sub(10, 5) == 5

def test_mul():
    assert mul(10, 5) == 50

def test_div():
    assert div(10, 5) == 2


def test_bank_account_initial_balance(bank_account):
    assert bank_account.balance == 50

def test_bank_account_initial_balance(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_account_deposit(bank_account):
    bank_account.deposit(100)
    assert bank_account.balance == 150

def test_bank_account_withdraw(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 40

def test_bank_account_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance) == 55

@pytest.mark.parametrize("deposit, withdraw, expected", [(500, 200, 350,), (500, 300, 250)])
def test_transactions(bank_account, deposit, withdraw, expected):
    bank_account.deposit(deposit)
    bank_account.withdraw(withdraw)
    assert bank_account.balance == expected

def test_insufficient_fund(bank_account):
     # This accepts only InsufficientFund Exception,
     # if some other exception is detected test won't pass
    with pytest.raises(InsufficientFund):
        bank_account.withdraw(200)
