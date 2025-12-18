# Sliding Window Rate Limiter

# A Rate Limiter

"""
A tool or mechanism that controls the number of requests or actions a
user or system can perform within a specific time frame.

# Use cases
-> Prevent system overload
-> Protect against Distributed Denial of Service (DDoS) attacks.
"""

## Sliding Window Rate Limiter Problem

"""
Design a rate-limiting system that follows the *sliding-window* algorithm.

You are given a class `SlidingWindow` with the following attributes:

-> `maxRequests`: The maximum number of requests that may occur in any 
                    contiguous window of length `windowSeconds` for a single client.
-> `windowSeconds`: The length (in seconds) of the sliding time-window that 
                    is checked for each request.
-> Each client (identified by `clientId`) is tracked independently.

A request is allowed if, after discarding timestamps that are older than 
(`now` - `windowSeconds`), the client has made strictly fewer than 
`maxRequests` requests in the remaining window.


Implement the following methods:

- `SlidingWindow(max_requests: number, window_seconds: number) -> void`: 
    Initialize the data structure. Both arguments are optional.

- `allowRequest(client: string) -> boolean`: Record the request if it is allowed 
    and return `true`, otherwise return `false` (nothing is recorded).

- `getRemainingRequests(client: string) -> int`: Return the number of additional 
    requests the client may still make in the current window (a non-negative integer).

Example 1:

Input:
["SlidingWindow", "allowRequest", "getRemainingRequests", "allowRequest", "getRemainingRequests", "allowRequest"]
[[2, 60],         ["123"],        ["123"],                ["123"],        ["123"],                ["123"]]

Output:
[null, true, 1, true, 0, false]

Explanation:

# 1 - Initialize the rate-limiter
sw = SlidingWindow(max_requests=2, window_seconds=60)      # → null

# 2 - First request inside the window ✓ allowed
sw.allowRequest("123")                                    # → true
# window now contains 1 timestamp

# 3 - 1 request remains available in the same 60-second window
sw.getRemainingRequests("123")                            # → 1

# 4 - Second request within the window ✓ allowed
sw.allowRequest("123")                                    # → true

Constraints:

- `1 ≤ maxRequests ≤ 10^3`
- `1 ≤ windowSeconds ≤ 10^3`
- Up to `10^5` total calls to `allowRequest` and `getRemainingRequests`.
- `clientId` is a non-empty ASCII string of length ≤ 64.
- Assume the judge calls the methods in *real time*; any two successive 
    calls are at least 0 ms apart.
"""
from collections import defaultdict
from threading import Lock
import time

class SlidingWindow:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_timestamps = defaultdict(list)
        self.lock = Lock()

    # Note: clientId can be any of userId, IP, API token, etc.
    def allow_request(self, client_id: str)-> bool:
        current_time = time.time()
        with self.lock:
            self._clean_old_requests(client_id)
            if len(self.request_timestamps[client_id]) < self.max_requests:
                self.request_timestamps[client_id].append(current_time)
                return True
            return False

    def _clean_old_requests(self, client_id: str):
        current_time = time.time()
        cuttoff_time = current_time - self.window_seconds
        self.request_timestamps[client_id] = \
            [ts for ts in self.request_timestamps[client_id] if ts >= cuttoff_time]

    def get_remaining_requests(self, client_id: str):
        with self.lock:
            self._clean_old_requests(client_id)
            return max(0, self.max_requests - len(self.request_timestamps[client_id]))

# n - number of users
# m - maxRequest
# `get_remaining_requests` and `allow_request` - O(m) -> O(1) Amortized - Time complexity
# O(n * m) - Space complexity