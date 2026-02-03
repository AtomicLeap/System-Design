## 📌 System Design

This repository is an attempt to curate my journey in learning system design.
It contains links to resources I stumbled upon in my quest to learn system design that I find very useful and want to keep handy to learn over and over until I have mastery of them.

# Core concepts
 - [Ashish Pratap Singh - System Design was HARD until I Learned these 30 Concepts](https://blog.algomaster.io/p/30-system-design-concepts)

# Handling LLD problems

1. Clarify requirements and core use cases.
2. Identify entities (How many classes will be there)
3. Create classes and their attributes 
4. Identify methods based on core use cases 
5. Define relationship between classes.
6. Implement necessary methods 
7. Exception handling ( errors, exception, edge cases, unexpected input)

# Handling HLD problems:

1. Identify requirements
    - Functional Requirements [that defines the functions of the system]
    - Non-Functional Requirements [that define the qualities and scale of   
        the system]
2. Define the Core Entities of the System
3. Define the API Design/Interfaces of the System
4. Do a High Level Design
5. Do a Deep Dive


# SOLID Principles

SOLID is an acronym that represents a set of five design principles coined by Robert C. Martin (Uncle Bob). These principles promote modular, maintainable, and extensible code:

- Single Responsibility Principle (SRP): A class should have only one reason to change.

- Open/Closed Principle (OCP): Software entities should be open for extension but closed for modification.

- Liskov Substitution Principle (LSP): Subtypes must be substitutable for their base types.

- Interface Segregation Principle (ISP): Clients should not be forced to depend on interfaces they do not use.

- Dependency Inversion Principle (DIP): High-level modules should not depend on low-level modules; both should depend on abstractions.

# ACID Properties of a Database

1. Atomicity - All or nothing. Commit all parts of a transaction or nothing.
2. Consistency - Preserve database invariants (rules). This is done by 
                    automating checks for constraints violations during transactions and cancelling such transactions that violate contraints(rules).
3. Isolation - Concurrent transactions are isolated from each other.
4. Durability - When a transaction is committed, it is permanent, even if 
                    the database crashes or losses power right after. In distributed databases, it means writting/replicating data accross multiple nodes so if one node goes down, we don't lose any committed transaction.

### Summary
- Atomicity - It rolls back failed transaction.
- Consistency - It follows the rules.
- Isolation - It prevents interference.
- Durability - It makes sure commit sticks.