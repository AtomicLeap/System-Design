# Account Balance Tracker

"""
A simple in-memory ledger that keeps track of every user's cash 
balance while processing a stream of textual transactions.

Supported transactions:
+-----------+----------------------------------------------+----------------------------------------+
| Kind      | Format                                       | Effect                                 |
+-----------+----------------------------------------------+----------------------------------------+
| Deposit   | "DEPOSIT <User> <Amount>"                    | Increase user's balance by amount      |
| Withdraw  | "WITHDRAW <User> <Amount>"                   | Decrease user's balance by amount      |
| Transfer  | "TRANSFER <FromUser> <ToUser> <Amount>"      | Move amount from FromUser to ToUser    |
+-----------+----------------------------------------------+----------------------------------------+

Note: User names are case-insensitive; balances are stored per unique
name (e.g. "alice", "ALICE", "Alice" all map to Alice).

Implement the following methods:

- `AccountBalanceTracker()` -> `void`: Construct an empty tracker (all balances 0).

- `processTransactions(transactions: string[])` -> `void`: Apply a batch of 
    transaction lines in order. Lines that are blank, malformed, or would 
    over-draw a balance are ignored.

- `getUserBalance(user: string)` -> `number`: Return the user's current balance.

Example 1:

Input:

operations = ["AccountBalanceTracker", "processTransactions", "getUserBalance", 
                "getUserBalance"]

arguments = [[],
             ["DEPOSIT Alice 100",
              "WITHDRAW Alice 30",
              "DEPOSIT Bob 50",
              "TRANSFER Alice Bob 50",
              "WITHDRAW Bob 120"],
             ["Alice"],
             ["Bob"]]

Output: [null, null, 20, 100]

Explanation:

1. `AccountBalanceTracker()` → tracker starts empty.

2. `processTransactions([...])` applies the five lines in order:

- DEPOSIT Alice 100 → Alice = 100  
- WITHDRAW Alice 30 → Alice = 70  
- DEPOSIT Bob 50 → Bob = 50  
- TRANSFER Alice Bob 50 → Alice = 20, Bob = 100  
- WITHDRAW Bob 120 → ignored (insufficient funds), Bob stays 100  

The method returns null (void).

3. `getUserBalance("Alice")` → 20  

4. `getUserBalance("Bob")` → 100  

Constraints:

- `1 <= number of transactions <= 10^4`
- `1 <= amount <= 10^4`
- At most `10^4` total calls will be made to `processTransactions`, and `getUserBalance`
- All user names are non-empty alphanumeric strings

"""

# Solution

from collections import defaultdict

class AccountBalanceTracker:
    def __init__(self):
        self.accounts = defaultdict(int)

    def _parse_three_part_operation(self, parts: str):
        operation = parts[0].upper()
        user = parts[1].title()
        amount = int(parts[2])
        return operation, user, amount
    
    def _parse_four_part_operation(self, parts: str):
        operation = parts[0].upper()
        transferrer = parts[1].title()
        transferree = parts[2].title()
        amount = int(parts[3])
        return operation, transferrer, transferree, amount
    
    def _process_transaction(self, parts: str):
        if len(parts) == 3:
            operation, user, amount = \
                self._parse_three_part_operation(parts)
            
            if operation == 'DEPOSIT':
                self.accounts[user] += amount
            elif operation == 'WITHDRAW':
                if amount <= self.accounts[user]:
                    self.accounts[user] -= amount
                else:
                    raise ValueError(f"Insufficient balance for: {operation}")
            else:
                raise ValueError(f"Invalid operation: {operation}")
        elif len(parts) == 4:
            operation, transferrer, transferree, amount = \
                self._parse_four_part_operation(parts)

            if operation == 'TRANSFER':
                if amount <= self.accounts[transferrer]:
                    self.accounts[transferrer] -= amount
                    self.accounts[transferree] += amount
                else:
                    raise ValueError(f"Insufficient balance for: {operation}")
            else:
                raise ValueError(f"Invalid operation: {operation}")
        else:
            raise ValueError(f"Invalid number of parts: {len(parts)}")

    def process_transactions(self, transactions: str):
        for transaction in transactions:
            stripped_transaction = transaction.strip()
            if not stripped_transaction:
                continue
            parts = stripped_transaction.split(' ')
            if not 3 <= len(parts) <= 4:
                continue
            self._process_transaction(parts)

    def get_user_balance(self, user: str):
        if user not in self.accounts:
            raise ValueError(f"User {user} not found")
        return self.accounts[user]
