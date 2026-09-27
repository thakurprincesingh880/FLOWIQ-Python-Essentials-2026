# FLOWIQ - Viva / Demo Guide

## 30-second explanation

"FLOWIQ is a Python-based service-flow optimization prototype. A user creates a service request with urgency, impact and group size. The program calculates an explainable priority score, checks eligible service counters, assigns the request to the least-loaded counter, estimates waiting time, maintains the queue and can simulate how additional counters could affect waiting time. I used Python data structures, control flow, functions, modules/packages, itertools, NumPy and OOP from the Python Essentials syllabus."

## Likely viva questions

### 1. What real problem does your project solve?
It addresses inefficient waiting and uneven workload in service centers. The prototype helps route requests to suitable counters and compare service capacity options.

### 2. Why did you choose this problem?
Queues and limited service capacity appear in many settings. That makes the idea broad enough to become a reusable product instead of a one-purpose college application.

### 3. Is FLOWIQ an AI project?
No. The submitted version is a rule-based and calculation-based prototype. It does not claim machine learning or natural-language AI.

### 4. What is the main algorithm?
First identify counters that support the requested service. Then compare their projected workload. The least-loaded eligible counter is selected. Queue length and average service time are tie-breakers.

### 5. Where are lists used?
Counters keep their queue as a list. The center also stores service requests in a list.

### 6. Where are tuples used?
Counter service capabilities are stored as tuples to represent fixed capability information during the current run.

### 7. Where are sets used?
The capability comparison uses sets to find shared services between two counters.

### 8. Where are dictionaries used?
Dashboard output and structured analysis use dictionaries so values can be accessed by meaningful keys.

### 9. Why use `itertools.combinations()`?
It creates unique counter pairs for capability analysis without manually writing every pair.

### 10. Where is NumPy used?
NumPy arrays calculate sums, means and maximum values for queue/workload analytics and simulation results.

### 11. Where is inheritance used?
`Student` inherits from `Person`, and `UrgentRequest` inherits from `ServiceRequest`.

### 12. Where is method overriding used?
`Student.label()` overrides `Person.label()`, and `UrgentRequest.priority_bonus()` provides specialized behavior for urgent requests.

### 13. Where is encapsulation used?
`ServiceCounter` keeps the served-ticket count in a private attribute `__tickets_served` and exposes it using `tickets_served()`.

### 14. Where is operator overloading used?
`ServiceRequest.__lt__()` compares requests by priority so the queue can sort higher-priority requests first.

### 15. Where is a class method used?
`Person.total_people()` is a class method that reports the number of created people.

### 16. Where is a static method used?
`ServiceRequest.valid_rating()` and `ServiceCounter.valid_service_time()` are static methods for simple validation checks.

### 17. What does the what-if simulation mean?
It takes a sequence of service durations and routes each incoming job to the currently least-loaded simulated counter. It then compares average and maximum waiting time for different counter counts.

### 18. What are the limitations?
The current model uses sample data and simplified waiting-time assumptions. It has no real-time sensor input, database, network service or external business data.

### 19. How can this become a real company/product?
The current Python engine can later become the logic layer of a web/mobile service with accounts, a database, live tokens, notifications, business analytics and eventually predictive models. Those technologies are intentionally not implemented in this Python Essentials submission.

### 20. Why didn't you use advanced frameworks?
Because the submission is meant to demonstrate Python Essentials. The project focuses on strong problem decomposition and algorithms rather than adding technology that is outside the current course scope.

## Demo order

1. `python demo.py`
2. `python main.py`
3. Show dashboard.
4. Register an IT Support request.
5. Show smart counter recommendation.
6. Advance time.
7. Run what-if simulation.
8. Show shared-service pairs.
