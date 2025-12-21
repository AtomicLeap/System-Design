# Locker Allocation System

"""
Package pickup locations use lockers of various sizes to hold customer packages.

The system should be able to:

- Support lockers of various sizes.
- Each locker can be empty or occupied.
- Given a package size, we must pick the "smallest empty locker" whose size ≥ package size.
- We also need to release lockers and check their occupied status.

Implement the following methods:

- `Locker(lockerId: string, size: number) -> void`: Initialize a locker.
- `Package(packageId: string, size: number) -> void`: Initialize a package.
- `PickupLocation(lockers: [string, number][]) -> void`: Initialize with a list of 
    (locker_id, size) pairs (all start empty).
- `findAndAllocate(packageId: string, packageSize: number) -> Optional[string]`: 
    Return the ID of the smallest empty locker whose size ≥ packageSize 
    (most recently freed/inserted if tied), or `null` if none exists.
- `releaseLocker(lockerId: string) -> boolean`: If lockerId exists and is occupied, 
    free it and return `true`; otherwise return `false`.
- `checkLockerStatus(lockerId: string) -> boolean`: Return `true` if lockerId exists 
    and is occupied, otherwise `false`.

Example 1:

Input:
["PickupLocation", "findAndAllocate", "findAndAllocate", "releaseLocker", "findAndAllocate", "checkLockerStatus"]
[[["L1", "10"], ["L2", "10"], ["L3", "20"]], ["P100", 9], ["P101", 10], ["L2"], ["P102", 15], ["L3"]]

Output:
[null, "L2", "L1", true, "L3", true]

Explanation:
PickupLocation pl = new PickupLocation([["L1","10"], ["L2","10"], ["L3","20"]]);
// All lockers (L1, L2 of size 10; L3 of size 20) start empty

pl.findAndAllocate("P100", 9);   // returns "L2"
// smallest size ≥9 is 10; among [L1,L2], pick the most recently added/freed → L2

pl.findAndAllocate("P101", 10);  // returns "L1"
// now only L1 of size 10 remains empty

pl.releaseLocker("L2");          // returns true
// frees up L2 (size 10) again

Constraints:

- `1 <= number of lockers <= 10^4`
- `1 <= size of each locker, size of each package <= 10^4`
- All `locker_id` and `packageId` are non-empty strings of alphanumeric characters.
- At most `10^4` total calls will be made to `findAndAllocate`, `releaseLocker`, 
    and `checkLockerStatus`.

"""
from bisect import bisect_left, insort

class Locker:
    def __init__(self, locker_id: str, size: int):
        self.id = locker_id
        self.size = size
        self.occupied = False

class Package:
    def __init__(self, package_id: str, size: int):
        self.id = package_id
        self.size = size

class PickUpLocation:
    def __init__(self, lockers: list[Locker]):
        # Map: locker_id -> Locker object
        self.lockers_map = { locker.id: locker for locker in lockers }
        # Map: size -> list of empty locker IDs
        self.available = {}
        # Sorted list of distinct sizes currently available
        self.sizes = []
        # Map: locker_id -> package_id (occupied)
        self.allocated = {}

        # Build "available" buckets and sorted sizes list
        for locker in lockers:
            if not locker.occupied:
                self.available.setdefault(locker.size, []).append(locker.id)
            self.sizes = sorted(self.available.keys())

    def find_and_allocate(self, package: Package) -> list[str] | None:
        # 1. Find smallest size >= package.size via binary search
        idx = bisect_left(self.sizes, package.size)
        if idx == len(self.sizes):
            return None # No available locker big enough
        
        chosen_size = self.sizes[idx]
        locker_list = self.available[chosen_size]
        # 2. Pop one locker ID (LIFO within same size)
        locker_id = locker_list.pop()

        # 3. If this was the last of that size, remove it from available and sizes
        if not locker_list:
            del self.available[chosen_size]
            self.sizes.pop(idx)

        # 4. Mark it as occupied
        locker_obj = self.lockers_map[locker_id]
        locker_obj.occupied = True
        self.allocated[locker_id] = package.id
        return locker_id

    def release_locker(self, locker_id: str) -> bool:
        locker = self.lockers_map.get(locker_id)
        if not locker or not locker.occupied:
            return False # Invalid Id or Locker already empty
        
        # Mark it empty and remove from allocated map
        locker.occupied = False
        self.allocated.pop(locker_id, None)

        # Insert it back into available[size]
        size_bucket = self.available.get(locker.size)
        if size_bucket is not None:
            size_bucket.append(locker_id)
        else:
            # First empty in this size -> create a new bucket and re-insert into sizes
            self.available[locker.size] = [locker_id]
            insort(self.sizes, locker.size)
        return True

    def check_locker_status(self, locker_id: str) -> bool:
        locker = self.lockers_map.get(locker_id)
        if not locker:
            return False # Nonexistent ID
        return locker.occupied
        

# Time Complexity:

"""
- `findAndAllocate`: `O(log n)` → binary search + list operations
- `releaseLocker`: `O(log n)` → binary insertion to maintain sorted order
- `checkLockerStatus`: `O(1)` → hash map lookup
"""

# Space Complexity:

"""
- `O(n)` where `n` is the number of lockers

The bottleneck is maintaining the sorted sizes list, which requires 
    `O(log n)` operations for insertion/removal.
"""
