
import cookbook

# +-------------------------------------------------+
# |  Categorize New Transactions  |
# +-------------------------------------------------+-------------------------------------
print("\n****** Categorizing New Transactions ******\n")
category = ''
transactions = cookbook.get_uncategorized_transactions()
for i, transaction in enumerate(transactions):
  category = cookbook.categorize(transaction)
  cookbook.log_transaction(transaction, update=True)
  if category != 'unknown': print(f"t_{i}: ", transaction)


print("\n****** Attempting to Re-Categorize Unknown Transactions ******\n")
transactions = cookbook.get_unknown_transactions()
for i, transaction in enumerate(transactions):
  if cookbook.categorize(transaction) != 'unknown':
    print("CATEGOTRY:",  cookbook.categorize(transaction))
    cookbook.log_transaction(transaction, update=True)
    print(f"t_{i}: ", transaction)
  

# +-------------------------------------------------+
# | Print Unknown Transactions  |
# +-------------------------------------------------+-------------------------------------
print("\n****** Uncategorized Transactions ******\n")

unknown_transactions = cookbook.get_unknown_transactions()
for transaction in unknown_transactions:
  print(transaction)
