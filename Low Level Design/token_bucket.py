# Token bucket Rate Limiter

# A Rate Limiter

"""
A tool or mechanism that controls the number of requests or actions a
user or system can perform within a specific time frame.

# Use cases
-> Prevent system overload
-> Protect against Distributed Denial of Service (DDoS) attacks.
"""

## Token Bucket Rate Limiting Problem

"""

Design a rate-limiting system that follows the "token-bucket" algorithm.
You are given a class `TokenBucket` with the following behavior:

- `capacity`: The maximum number of tokens that can be stored in the bucket.
- `refill_rate`: The (possibly fractional) number of tokens added to the bucket 
    every second.
- Each user has an independent bucket identified by their `user_id`.

A request "consumes" a specified number of tokens.
A request is "allowed" if "after refilling up to the current time" the user's 
bucket still contains at least that many tokens.

Implement the following methods:
- `TokenBucket(capacity = 5, refill_rate = 1) -> void`: Initialize the data structure. 
    Both arguments are optional; defaults shown.
- `canRequest(user: string, required_tokens = 1) -> boolean`: 
    Return `true` and deduct `required_tokens` if the user currently has enough tokens; 
    otherwise return `false` (no tokens are removed).
- `availableTokens(user: string) -> int`: Return the integer number of full tokens 
    the user has at this moment.

Example 1:

Input:
["TokenBucket", "canRequest", "availableTokens", "canRequest", "availableTokens"]
[[],
 ["123"],
 ["123"],
 ["123", 5],
 ["123"]]

Output:
[null, true, 4, false, 4]

Explanation:

# 1 - Initialize the rate-limiter (capacity = 5, refill_rate = 1)
tb = TokenBucket()                                   # → null

# 2 - First request consumes 1 token (5 → 4) ✓ allowed
tb.canRequest("123")                                # → true

# 3 - Query remaining full tokens (fractional part truncated) → 4
tb.availableTokens("123")                           # → 4

# 4 - Attempt to consume 5 tokens (only 4 available) ✗ denied
tb.canRequest("123", 5)                             # → false

# 5 - Bucket state unchanged since request was denied
tb.availableTokens("123")                           # → 4


Constraints:

- `1 ≤ capacity ≤ 10^3`
- `0 < refill_rate ≤ 10^3`
- Up to `10^5` total calls to `canRequest` and `availableTokens`.
- `user_id` is a non-empty ASCII string of length ≤ 64.
"""

from collections import defaultdict
from threading import Lock
import time

class TokenBucket:
    def __init__(self, capacity = 5.0, refill_rate = 1.0):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = defaultdict(lambda: self.capacity)
        self.last_refill_time = defaultdict(lambda: time.time())
        self.lock = Lock()

    def _refill(self, user_id: str):
        current_time = time.time()
        elapsed_time = current_time - self.last_refill_time[user_id]
        new_tokens = self.refill_rate * elapsed_time
        self.tokens[user_id] = min(self.capacity, self.tokens[user_id] + new_tokens)
        self.last_refill_time[user_id] = current_time

    def can_request(self, user_id: str, required_tokens = 1) -> bool:
        with self.lock:
            self._refill(user_id)
            if self.tokens[user_id] >= required_tokens + 1e-6: # Epsilon to prevent rounding error
                self.tokens -= required_tokens
                return True
            return False

    def available_tokens(self, user_id: str) -> int:
        with self.lock:
            self._refill(user_id)
            return int(self.tokens[user_id] + 1e-6)

# n - Number of users        
# can_request and available_tokens  - O(1) - Time complexity
# O(n) - Space comlexity
