# Lock System Recipe

"""
This is a shared, mutable in-memory data structure, accessed by multiple 
threads concurrently.

That is exactly why Lock exists in rate limiting systems.
"""

# What is a Lock?

"""
A Lock is a mutual-exclusion (mutex) primitive used to prevent race conditions 
when multiple threads access shared state.

A lock guarantees that only one thread at a time can execute a critical section of code.
"""

# I Python:

"""
from threading import Lock
lock = Lock()


lock.acquire() # → enter critical section

lock.release() # → exit critical section
"""

# Or safely:

"""
with lock:
    # critical section
"""

# Why is a Lock needed in the Sliding Window Rate Limiter code?

"""
->  Shared mutable state - self.request_timestamps = defaultdict(list)
This dictionary:
    -   Is shared across threads
    -   Is mutable
    -   Stores lists, which are also mutable

Multiple threads may:
    -   Append timestamps
    -   Remove old timestamps
    -   Check list length

Without a Lock → race condition

Example scenario:

Thread A:
timestamps = request_timestamps[user]
len(timestamps) == 9

Thread B (at same time):
timestamps.append(now)

Thread A resumes:
timestamps.append(now)

Result:
11 requests allowed instead of 10

    -   Rate limiter broken
    -   Inconsistent state
This is a classic race condition.
"""

# What exactly does the Lock protect?

"""
The lock protects the critical section where:

    -   Reading timestamps
    -   Filtering expired timestamps
    -   Appending new timestamps

Updating the dictionary

Example (what you would write later):

with self.lock:
    timestamps = self.request_timestamps[key]
    timestamps = [t for t in timestamps if t > cutoff]
    if len(timestamps) >= self.max_requests:
        return False
    timestamps.append(now)


Everything inside with self.lock: is atomic from a thread perspective.
"""

# Importance of Lock (why this is NOT optional)

"""
1. Prevents race conditions
Without a lock:
    -   Incorrect request counts
    -   Rate limiting bypass
    -   Undefined behavior

2. Ensures data consistency
The timestamps list must reflect true ordering and counts.

3. Ensures correctness under load
    -   Under low traffic, bugs may not appear.
    -   Under high concurrency, the system fails catastrophically.

4. Required even with Python's GIL
"""

# Important interview point:

"""
The GIL does NOT protect your data structures.
The GIL:
    -   Prevents multiple threads from executing Python bytecode simultaneously.
    -   Does NOT make compound operations atomic

Example:

timestamps.append(now)
len(timestamps)

These are multiple bytecode operations → not atomic.
"""

# Why a single global Lock (design tradeoff)

"""
-> Pros
    -   Simple
    -   Correct
    -   Easy to reason (think) about

-> Cons
    -   Limits concurrency
    -   All users contend for same lock
"""

# Better designs (advanced)

"""
    -   Lock per key (dict[key] -> Lock)
    -   Sharded locks
    -   Redis-based rate limiting
    -   Token bucket with atomic counters

But for an in-memory sliding window, a single lock is acceptable.
"""

# What happens if you remove the Lock?

"""
------------------------------------------------------------------
Problem	                            Outcome
------------------------------------------------------------------
Race conditions	                    Requests bypass limit
Lost updates	                    Incorrect timestamps
Corrupted lists	                    Runtime errors
Non-deterministic behavior	        Impossible to debug

This is one of the worst classes of bugs in production.
"""

# Lock vs alternatives (important distinction)

"""
------------------------------------------------------------------
Mechanism	                        Use case
------------------------------------------------------------------
Lock	                            Threads, shared memory
Semaphore	                        Limit concurrent access count
RLock	                            Re-entrant locking
Atomic ops	                        Simple counters
Redis	                            Distributed locking
Message queues	                    Async decoupling
System Design takeaway

This code shows:
    -   Awareness of concurrency
    -   Understanding of thread safety
    -   Correct use of mutex for critical sections

That’s a strong signal in backend interviews.
"""
