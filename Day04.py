class Account:
    def __init__(self, owner, account_number, balance):
        # Step 1: Encapsulated private attribute __balance
        self.owner = owner
        self.account_number = account_number
        self.__balance = balance

    # Step 2: Read-only property to access private balance
    @property
    def balance(self):
        return self.__balance

    # Step 3 & 4: Validated deposits (reject negative/zero)
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"[{self.owner}] Deposited ${amount:.2f}. New balance: ${self.__balance:.2f}")
        else:
            print(f"[{self.owner}] Error: Deposit amount must be positive.")

    # Step 3 & 4: Validated withdrawals (reject negative/zero and overdrafts)
    def withdraw(self, amount):
        if amount <= 0:
            print(f"[{self.owner}] Error: Withdrawal amount must be positive.")
        elif amount > self.__balance:
            print(f"[{self.owner}] Error: Insufficient funds. Overdraft rejected.")
        else:
            self.__balance -= amount
            print(f"[{self.owner}] Withdrew ${amount:.2f}. New balance: ${self.__balance:.2f}")


# Step 5: Create two accounts and run transactions
if __name__ == "__main__":
    print("--- Testing Account 1 ---")
    acc1 = Account("Hermella", "ACC001", 1000)
    acc1.deposit(500)       # Valid deposit
    acc1.withdraw(200)      # Valid withdrawal
    acc1.withdraw(2000)     # Overdraft test (should fail)
    acc1.deposit(-50)       # Negative deposit test (should fail)
    print(f"Final balance for {acc1.owner}: ${acc1.balance:.2f}\n")

    print("--- Testing Account 2 ---")
    acc2 = Account("Abebe", "ACC002", 500)
    acc2.deposit(250)       # Valid deposit
    acc2.withdraw(800)      # Valid withdrawal
    print(f"Final balance for {acc2.owner}: ${acc2.balance:.2f}")