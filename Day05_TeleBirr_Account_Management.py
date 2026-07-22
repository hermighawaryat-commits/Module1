class Account:
    def __init__(self, owner, account_number, balance):
        self.owner = owner
        self.account_number = account_number
        self._balance = balance  # Using _balance so child classes can modify it directly

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"[{self.owner}] Deposited ${amount:.2f}. New balance: ${self._balance:.2f}")
        else:
            print(f"[{self.owner}] Error: Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount <= 0:
            print(f"[{self.owner}] Error: Withdrawal amount must be positive.")
        elif amount > self._balance:
            print(f"[{self.owner}] Error: Insufficient funds. Overdraft rejected.")
        else:
            self._balance -= amount
            print(f"[{self.owner}] Withdrew ${amount:.2f}. New balance: ${self._balance:.2f}")

    # Base statement method
    def statement(self):
        print(f"[Standard Account] Owner: {self.owner} | Acc #: {self.account_number} | Balance: ${self._balance:.2f}")


# Step 2: SavingsAccount subclass
class SavingsAccount(Account):
    def __init__(self, owner, account_number, balance, interest_rate):
        super().__init__(owner, account_number, balance)
        self.interest_rate = interest_rate  # e.g., 0.05 for 5%

    def add_interest(self):
        interest = self._balance * self.interest_rate
        self._balance += interest
        print(f"[{self.owner}] Added interest of ${interest:.2f}. New balance: ${self._balance:.2f}")

    # Step 4: Overridden statement method
    def statement(self):
        print(f"[Savings Account] Owner: {self.owner} | Acc #: {self.account_number} | Balance: ${self._balance:.2f} | Rate: {self.interest_rate * 100:.1f}%")


# Step 3: CurrentAccount subclass
class CurrentAccount(Account):
    def __init__(self, owner, account_number, balance, overdraft_limit):
        super().__init__(owner, account_number, balance)
        self.overdraft_limit = overdraft_limit

    # Overridden withdraw method to allow overdraft up to the limit
    def withdraw(self, amount):
        if amount <= 0:
            print(f"[{self.owner}] Error: Withdrawal amount must be positive.")
        elif amount > self._balance + self.overdraft_limit:
            print(f"[{self.owner}] Error: Overdraft limit of ${self.overdraft_limit:.2f} exceeded.")
        else:
            self._balance -= amount
            print(f"[{self.owner}] Withdrew ${amount:.2f}. New balance: ${self._balance:.2f}")

    # Step 4: Overridden statement method
    def statement(self):
        print(f"[Current Account] Owner: {self.owner} | Acc #: {self.account_number} | Balance: ${self._balance:.2f} | Overdraft Limit: ${self.overdraft_limit:.2f}")


# --- Step 5: Polymorphic Loop ---
if __name__ == "__main__":
    # Create a mixed list of objects
    accounts = [
        Account("Alice", "ACC-01", 1000.00),
        SavingsAccount("Bob", "SAV-02", 5000.00, interest_rate=0.03),
        CurrentAccount("Charlie", "CUR-03", 200.00, overdraft_limit=500.00)
    ]

    print("=== Account Statements ===")
    # One loop handling different class types (Polymorphism)
    for acc in accounts:
        acc.statement()