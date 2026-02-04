# Design Twitter (X)

"""
--------------   ---------------   --------------    -------------------   -----------
|Requirements|-->|Core Entities|-->|API/Interface|-->|High Level Design|-->|Deep Dive|
--------------   ---------------   --------------    -------------------   -----------
"""

# Requirements
"""
1. Get on the same page with your interviewer.
2. Know and understand what you want to build (The features you are going to design). 
"""
# -> Functional Requirements (Functionalities of the system)
"""
A user should be able to:
1. Create an account and login.
2. Create, Read, Edit/Update and Delete (CRUD) a tweet.
3. Follow other users.
4. View the timeline of tweets from their following.
5. Like, reply and retweet.
6. Search for a tweet.
"""

# -> Non-Functional Requirements (Qualities of the system)
"""
1. Scale to support 100+ millions of users and atleast 50+ million DAU.
2. Handle a high volume of tweets, likes and retweets.
3. Highly available (99.999% uptime)
4. Security and privacy of users' data.
5. Low latency (<=100ms load time)
"""

# Core Entities
"""
1. Tweet
2. User
3. Follower
4. Following
"""

# API/Interface

# Load Balancer Routing 
# Routing Algorithms
"""
1. Round-Robin -> Rotates request evenly among all servers.
2. Least connections -> Sends requests to the server with the  
                        fewest connections.
3. IP Hash -> Routes based on IP, ensuring the same IP gets the 
                same server for each request.
"""

# Types of Load balancers (based on Application Layers)
#2. Layer
"""
1. Layer 4: Transport Layer (e.g TCP)
2. Layer 7: Application Layer(e.g HTTPS). Routes based on contents
            like url and HTTP headers.
"""

# Security
"""
1. Authentication and Authorization - Handled by Auth Service.
2. Data Encryption - User's data both at rest in DB and in transit 
    should be encrypted. We use HTTPS to encrypt data in transit from 
    client to DB. Most databases have encryption mechanisms for data 
    they handle.
3. Rate Limiting - To prevent DDoS Attacks we do IP Rate Limiting, to
    prevent any single user or BOT from overwhelming our system.
4. Input Validation - Sanitize inputs from client to prevent SQL Injection, 
    Cross site Scripting (XSS), or other malicious inputs from client.
"""

# Monitoring
"""
1. Health checks - Real-time health checks. Utilize tools like Promethius, and 
    integrate with Grafana. We could also use DataDog. Used for monitoring and 
    providing real-time metrics.
2. Logging - Every action from tweeting to user log-in should be logged. This is to  
    aid debugging and preventing potential security threats. We use ELK stack - 
    (Elastic Search, LogStash and Kibana). Elastic search stores our logs, LogStash
    will process the logs and Kibana provides a visual interface to analyze these logs.
3. Alerts - Real-time alerts. If it is a sudden urge in traffic, or multiple failed 
    log-in attempts, we should be notified. Integrating tools like Alert Manager,
    or Pager-Duty with ELK can help send email, or notification to Slack channels etc
    so that we are immediately notified when something wrong happens.
"""

# Testing
"""
1. Load testing - Before introducing any feature we need to see how our existing services 
    will hold up under the new pressure. This helps us to pin-point bottlenecks and prevent 
    potential failures.
2. Automated testing - Given our microservices architecture, it is partcularly important 
    that our services integrate seemlessly. Everytime there is a code change, our CI/CD pipeline
    tools such as Jenkins, or Github actions should automatically run both Unit tests (Which 
    checks our individual components) and Integration tests (which ensures the services 
    communicate effectively).
3. Backup and Recovery - Our data are invaluable, so regular back-ups are non-negotiable.
    We need to periodically test our recovery process. This is to ensure in the event of an 
    unlikely system failure we can restore our system back quickly.
"""
