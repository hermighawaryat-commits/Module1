# 1. Observer
class SMSAlert:
    def update(self, event):
        print(f"[SMS Alert] {event}")

# 2. Account Family (with History Stack) 
class Account:
    def __init__(self, owner, number, balance=0):
        self.owner = owner
        self.number = number
        self._balance = balance
        self._observers = []
        self.history = []  # Stack for undoing

    def subscribe(self, observer):
        self._observers.append(observer)

    def _notify(self, event):
        for obs in self._observers:
            obs.update(event)

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self.history.append(("deposit", amount))  # Push to stack
            self._notify(f"{self.owner} deposited ${amount:.2f}. Balance: ${self._balance:.2f}")

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            self.history.append(("withdraw", amount))  # Push to stack
            self._notify(f"{self.owner} withdrew ${amount:.2f}. Balance: ${self._balance:.2f}")

    def undo_last(self):
        if not self.history:
            print(f"[{self.owner}] Nothing to undo.")
            return

        action, amount = self.history.pop()  # Pop from stack
        if action == "deposit":
            self._balance -= amount
        elif action == "withdraw":
            self._balance += amount
        self._notify(f"UNDONE {action} of ${amount:.2f}. Balance: ${self._balance:.2f}")

    def statement(self):
        print(f"[Account] {self.owner} | #{self.number} | Balance: ${self._balance:.2f}")

class SavingsAccount(Account):
    def __init__(self, owner, number, balance=0, interest_rate=0.03):
        super().__init__(owner, number, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self._balance * self.interest_rate
        self._balance += interest
        self.history.append(("deposit", interest))
        self._notify(f"{self.owner} earned ${interest:.2f} interest. Balance: ${self._balance:.2f}")

class CurrentAccount(Account):
    def __init__(self, owner, number, balance=0, overdraft_limit=500.00):
        super().__init__(owner, number, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if 0 < amount <= self._balance + self.overdraft_limit:
            self._balance -= amount
            self.history.append(("withdraw", amount))
            self._notify(f"{self.owner} withdrew ${amount:.2f}. Balance: ${self._balance:.2f}")

# 3. Account Factory
class AccountFactory:
    @staticmethod
    def create(kind, owner, number, balance=0):
        if kind == "savings":
            return SavingsAccount(owner, number, balance)
        if kind == "current":
            return CurrentAccount(owner, number, balance)
        raise ValueError(f"Unknown type: {kind}")


# 4. Account Registry (O(1) Dict Lookup) 
class AccountRegistry:
    def __init__(self):
        self._accounts = {}  # {account_number: account_object}

    def add(self, account):
        self._accounts[account.number] = account

    def find(self, number):
        return self._accounts.get(number)  # O(1) lookup

    def list_all(self):
        return list(self._accounts.values())

# 5. Execution 
if __name__ == "__main__":
    sms = SMSAlert()
    registry = AccountRegistry()

    # Create & subscribe accounts
    sav = AccountFactory.create("savings", "Almaz", "CBE-1", 1500)
    cur = AccountFactory.create("current", "Bekele", "CBE-2", 500)
    sav.subscribe(sms)
    cur.subscribe(sms)

    # Register accounts
    registry.add(sav)
    registry.add(cur)

    # Test O(1) find & undo stack
    acc = registry.find("CBE-1")
    acc.deposit(500)   # Balance -> 2000
    acc.withdraw(200)  # Balance -> 1800
    acc.undo_last()    # Undoes withdraw -> Balance back to 2000