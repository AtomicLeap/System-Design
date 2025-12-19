# Access Management System

"""
Design an Access Management system that supports the following:

- "Role-based access control (RBAC)" with three primary entities: 
    `Role`, `Permission`, and `User`.
- Each role has a unique `name` and a set of permissions 
    (e.g. `"delete_user"`, `"ban_user"`).
- A user can possess multiple roles; roles may be shared by many users.
- A user is considered to have a permission if any of their roles contains 
    that permission.

- Core operations:
  - Create new roles.
  - Grant additional permissions to an existing role.
  - Assign or revoke roles for a user at any time.
  - Check whether a user currently has a given permission.

Implement the following methods:

- `AccessManager()` → `void`: Initialize the internal role registry and 
        user-to-role mapping.
- `createRole(name: string)` → `void`: Add a new role.
- `grantPermission(role: string, permission: string)` → `void`: Add the permission 
        to the specified role.
- `assignRole(user: string, role: string)` → `void`: Give the role to the user 
        (idempotent).
- `revokeRole(user: string, role: string)` → `void`: Remove the role from the 
        user (no-op if the user does not hold it).
- `hasPermission(user: string, permission: string)` → `boolean`: Return `true` if 
        the user currently has the permission, otherwise `false`.

Example 1:

Input:
["AccessManager", "createRole", "grantPermission", "assignRole", "hasPermission", 
    "hasPermission", "hasPermission", "revokeRole", "hasPermission"]
[[], ["admin"], ["admin", "delete_user"], ["alice", "admin"], 
    ["alice", "delete_user"], ["alice", "ban_user"], ["bob", "delete_user"], 
    ["alice", "admin"], ["alice", "delete_user"]]

Output:
[null, null, null, null, true, false, false, null, false]

Explanation:

# 1 - Initialize the system
ams = AccessManager()                               # → null

# 2 - Define an "admin" role and grant it a permission
ams.createRole("admin")                             # → null
ams.grantPermission("admin", "delete_user")         # → null

# 3 - Give the role to Alice
ams.assignRole("alice", "admin")                    # → null

# 4 - Permission queries
ams.hasPermission("alice", "delete_user")           # → true
ams.hasPermission("alice", "ban_user")              # → false (not granted)
ams.hasPermission("bob", "delete_user")             # → false (Bob has no roles)

# 5 - Revoke Alice’s role and query again
ams.revokeRole("alice", "admin")                    # → null
ams.hasPermission("alice", "delete_user")           # → false


Constraints:

- `1 ≤ number of roles, number of users ≤ 10^4`
- At most `10^5` total calls will be made to `createRole`, `grantPermission`, 
    `assignRole`, `revokeRole`, and `hasPermission`.
- All role names, user identifiers, and permission strings are non-empty ASCII 
    strings of length ≤ 64.
"""
from dataclasses import dataclass, field
from typing import Set, Dict

@dataclass
class Role:
    name: str
    permissions: Set[str] = field(default_factory=set)

class AccessManager:
    def __init__(self) -> None:
        self._roles: Dict[str, Role] = {} # role_name -> Role object
        self._user_roles: Dict[str, Set[str]] = {} # user_id -> { role_names }

    def create_role(self, name: str) -> None:
        if name in self._roles:
            raise ValueError(f'Role {name!r} already exists')
        self._roles[name] = Role(name)

    def _get_role(self, name: str) -> Role:
        try:
            return self._roles[name]
        except KeyError:
            raise ValueError(f'Unknown role: {name}') from None

    def grant_permission(self, role: str, permission: str) -> None:
        self._get_role(role).permissions.add(permission)

    def assign_role(self, user: str, role: str) -> None:
        self._get_role(role)
        self._user_roles.setdefault(user, set()).add(role)

    def revoke_role(self, user: str, role: str) -> None:
        self._user_roles.get(user, set()).discard(role)

    def has_permission(self, user: str, permission: str) -> bool:
        return any(
            permission in self._roles[role].permissions
            for role in self._user_roles.get(user, ())
            )
    
# - Time Complexity:

"""
  - `hasPermission`: `O(r)` where `r` is the number of roles held by the user.
  - All other methods are `O(1)` due to the use of hash maps and a hash set.
"""
# - Space Complexity:

"""
  - `O(r + p + a)`
    - `r` = number of roles
    - `p` = total permissions across all roles
    - `a` = total role-to-user assignments
"""

# Key optimization:

"""
Both roles and user-role mappings are maintained with hash maps, while each role’s 
permission list is a hash set.
"""