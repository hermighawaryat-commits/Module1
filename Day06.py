
# 1. OBSERVER PATTERN (Alert Service)

class SMSAlert:
    """Alert service operating as an observer (SRP)."""
    def update(self, event):
        print(f"[SMS Alert] {event}")

# 2. ACCOUNT FAMILY (Subject)

class Account:
    def __init__(self, owner, number, balance=0):
        self.owner = owner
        self.number = number
        self._balance = balance
        self._observers = []

    def subscribe(self, observer):
        self._observers.append(observer)

    def _notify(self, event):
        for obs in self._observers:
            obs.update(event)

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self._notify(f"{self.owner} deposited ${amount:.2f}. Balance: ${self._balance:.2f}")

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            self._notify(f"{self.owner} withdrew ${amount:.2f}. Balance: ${self._balance:.2f}")

    def statement(self):
        print(f"[Standard] {self.owner} | #{self.number} | Balance: ${self._balance:.2f}")


class SavingsAccount(Account):
    def __init__(self, owner, number, balance=0, interest_rate=0.03):
        super().__init__(owner, number, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self._balance * self.interest_rate
        self._balance += interest
        self._notify(f"{self.owner} earned ${interest:.2f} interest. Balance: ${self._balance:.2f}")

    def statement(self):
        print(f"[Savings] {self.owner} | #{self.number} | Balance: ${self._balance:.2f} | Rate: {self.interest_rate*100:.1f}%")


class CurrentAccount(Account):
    def __init__(self, owner, number, balance=0, overdraft_limit=500.00):
        super().__init__(owner, number, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if 0 < amount <= self._balance + self.overdraft_limit:
            self._balance -= amount
            self._notify(f"{self.owner} withdrew ${amount:.2f}. Balance: ${self._balance:.2f}")

    def statement(self):
        print(f"[Current] {self.owner} | #{self.number} | Balance: ${self._balance:.2f} | Overdraft: ${self.overdraft_limit:.2f}")

# 3. FACTORY PATTERN

class AccountFactory:
    @staticmethod
    def create(kind, owner, number, balance=0):
        if kind == "savings":
            return SavingsAccount(owner, number, balance)
        if kind == "current":
            return CurrentAccount(owner, number, balance)
        raise ValueError(f"Unknown type: {kind}")

# 4. EXECUTION

if __name__ == "__main__":
    sms = SMSAlert()

    # Create accounts via factory
    sav = AccountFactory.create("savings", "Almaz", "CBE-1", 1500)
    cur = AccountFactory.create("current", "Bekele", "CBE-2", 500)

    # Attach alerts
    sav.subscribe(sms)
    cur.subscribe(sms)

    # Perform operations
    sav.deposit(500)
    sav.add_interest()
    cur.withdraw(200)