transactions = {}

# 1. Read file with exception handling for missing files
try:
    with open("transactions.txt", "r") as f:
        for line in f:
            # Skip empty lines
            line = line.strip()
            if not line:
                continue

            # Parse 'Name, Amount'
            try:
                name, amount_str = line.split(",")
                name = name.strip()
                amount = float(amount_str.strip())

                # 2. Build dict mapping each customer to their total spend
                transactions[name] = transactions.get(name, 0.0) + amount
            except ValueError:
                print(f"Warning: Skipping malformed line -> '{line}'")

except FileNotFoundError:
    print("Error: The file 'transactions.txt' was not found.")
    exit()

# 3. Sort customers by total spend, highest first
sorted_transactions = sorted(
    transactions.items(), key=lambda item: item[1], reverse=True
)

# 4. Print each customer & total, and write to report.txt
print("\n--- Transaction Summary ---")

with open("report.txt", "w") as out:
    for customer, total in sorted_transactions:
        summary_line = f"{customer}: ${total:.2f}"
        
        # Print to terminal
        print(summary_line)
        
        # Write to output file
        out.write(summary_line + "\n")

print("\nReport successfully saved to 'report.txt'!")