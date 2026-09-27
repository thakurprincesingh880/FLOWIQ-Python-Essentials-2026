"""FLOWIQ - Standalone single-file version.

Run with: python FLOWIQ.py
"""

"""Core object-oriented models for FLOWIQ.

Designed for the VITyarthi Python Essentials syllabus:
- classes and constructors
- inheritance and method overriding
- encapsulation with private attributes
- classmethod and staticmethod
- lists, tuples and dictionaries
"""


class Person:
    """Base person model used to demonstrate inheritance."""

    people_created = 0

    def __init__(self, name, person_type="Customer"):
        self.name = name
        self.person_type = person_type
        Person.people_created += 1

    @classmethod
    def total_people(cls):
        return cls.people_created

    def label(self):
        return f"{self.person_type}: {self.name}"


class Student(Person):
    """A campus user who can raise a service request."""

    def __init__(self, name, student_id):
        super().__init__(name, "Student")
        self.student_id = student_id

    def label(self):
        return f"Student: {self.name} ({self.student_id})"


class ServiceRequest:
    """A service request/ticket inside FLOWIQ."""

    next_id = 1001

    def __init__(self, person, service, urgency, impact, group_size=1):
        self.request_id = ServiceRequest.next_id
        ServiceRequest.next_id += 1
        self.person = person
        self.service = service
        self.urgency = urgency
        self.impact = impact
        self.group_size = group_size
        self.waiting_minutes = 0
        self.status = "WAITING"
        self.assigned_counter = None

    @staticmethod
    def valid_rating(value):
        return 1 <= value <= 10

    def priority_bonus(self):
        """Base ticket gets no extra bonus."""
        return 0

    def priority_score(self):
        group_factor = min(self.group_size, 10)
        wait_factor = min(self.waiting_minutes, 60) * 0.20
        return (self.urgency * 5) + (self.impact * 3) + group_factor + wait_factor + self.priority_bonus()

    def priority_label(self):
        score = self.priority_score()
        if score >= 65:
            return "CRITICAL"
        if score >= 45:
            return "HIGH"
        if score >= 25:
            return "MEDIUM"
        return "LOW"

    def __lt__(self, other):
        """Operator overloading: higher priority sorts first."""
        return self.priority_score() > other.priority_score()

    def summary(self):
        counter = self.assigned_counter if self.assigned_counter else "Unassigned"
        return (
            f"#{self.request_id} | {self.service} | {self.priority_label()} "
            f"({self.priority_score():.1f}) | {self.status} | Counter: {counter}"
        )


class UrgentRequest(ServiceRequest):
    """Specialized request with a small escalation bonus."""

    def priority_bonus(self):
        return 8


class ServiceCounter:
    """Represents one service counter and its queue."""

    def __init__(self, counter_id, name, supported_services, average_service_minutes=5, active=True):
        self.counter_id = counter_id
        self.name = name
        self.supported_services = tuple(supported_services)
        self.average_service_minutes = average_service_minutes
        self.active = active
        self.queue = []
        self.__tickets_served = 0

    @staticmethod
    def valid_service_time(minutes):
        return minutes > 0

    def can_serve(self, service):
        return self.active and service in self.supported_services

    def workload_minutes(self):
        return len(self.queue) * self.average_service_minutes

    def add_request(self, request):
        self.queue.append(request)
        self.queue.sort()
        request.assigned_counter = self.name

    def serve_next(self):
        if not self.queue:
            return None
        request = self.queue.pop(0)
        request.status = "COMPLETED"
        self.__tickets_served += 1
        return request

    def tickets_served(self):
        return self.__tickets_served

    def utilization_band(self):
        count = len(self.queue)
        if count >= 8:
            return "HEAVY"
        if count >= 4:
            return "MODERATE"
        return "LIGHT"

    def __str__(self):
        return f"C{self.counter_id} - {self.name}"


class FlowCenter:
    """Main controller that manages counters and service requests."""

    def __init__(self, name="FLOWIQ Service Center"):
        self.name = name
        self.counters = []
        self.requests = []
        self.service_history = []

    def add_counter(self, counter):
        self.counters.append(counter)

    def add_request_record(self, request):
        self.requests.append(request)

    def find_counter(self, counter_id):
        for counter in self.counters:
            if counter.counter_id == counter_id:
                return counter
        return None

    def pending_requests(self):
        result = []
        for request in self.requests:
            if request.status == "WAITING":
                result.append(request)
        return result

    def total_pending(self):
        return len(self.pending_requests())

    def total_queue_workload(self):
        total = 0
        for counter in self.counters:
            total += counter.workload_minutes()
        return total


"""Decision and flow algorithms for FLOWIQ."""


def calculate_priority(request):
    """Return the request priority score and label."""
    return request.priority_score(), request.priority_label()


def eligible_counters(counters, service):
    """Return counters that can serve a requested service."""
    result = []
    for counter in counters:
        if counter.can_serve(service):
            result.append(counter)
    return result


def smart_counter_recommendation(counters, request):
    """Choose the counter with the lowest projected waiting workload.

    Tie-breakers:
    1. Lowest workload in minutes
    2. Shortest queue
    3. Smaller average service time
    """
    candidates = eligible_counters(counters, request.service)
    if not candidates:
        return None

    best = candidates[0]
    for counter in candidates[1:]:
        best_key = (best.workload_minutes(), len(best.queue), best.average_service_minutes)
        current_key = (counter.workload_minutes(), len(counter.queue), counter.average_service_minutes)
        if current_key < best_key:
            best = counter
    return best


def assign_request(counters, request):
    """Assign a request to the least-loaded eligible counter."""
    counter = smart_counter_recommendation(counters, request)
    if counter is None:
        return None
    counter.add_request(request)
    request.status = "WAITING"
    return counter


def estimate_wait(counter):
    """Estimate waiting time before the new request can be served."""
    return counter.workload_minutes()


def process_next(counter):
    """Serve the highest-priority request waiting at a counter."""
    return counter.serve_next()


def advance_time(counters, minutes):
    """Increase waiting time of all currently queued requests."""
    for counter in counters:
        for request in counter.queue:
            request.waiting_minutes += minutes
        counter.queue.sort()


def counter_snapshot(counters):
    """Return structured data for dashboard display."""
    rows = []
    for counter in counters:
        rows.append({
            "counter": counter.name,
            "queue": len(counter.queue),
            "workload_minutes": counter.workload_minutes(),
            "band": counter.utilization_band(),
            "served": counter.tickets_served(),
        })
    return rows


"""Analytics, simulation and combinations for FLOWIQ."""

from itertools import combinations
import numpy as np


def dashboard(counters, requests):
    """Use NumPy arrays for live queue statistics."""
    queue_lengths = []
    workloads = []
    completed = []
    waits = []

    for counter in counters:
        queue_lengths.append(len(counter.queue))
        workloads.append(counter.workload_minutes())
        completed.append(counter.tickets_served())

    for request in requests:
        if request.status == "COMPLETED":
            waits.append(request.waiting_minutes)

    if queue_lengths:
        queue_array = np.array(queue_lengths)
        workload_array = np.array(workloads)
        completed_array = np.array(completed)
    else:
        queue_array = np.array([0])
        workload_array = np.array([0])
        completed_array = np.array([0])

    if waits:
        wait_array = np.array(waits)
        avg_completed_wait = float(np.mean(wait_array))
    else:
        avg_completed_wait = 0.0

    return {
        "active_counters": len(counters),
        "total_waiting": int(np.sum(queue_array)),
        "total_workload_minutes": int(np.sum(workload_array)),
        "average_queue": float(np.mean(queue_array)),
        "maximum_queue": int(np.max(queue_array)),
        "tickets_served": int(np.sum(completed_array)),
        "average_completed_wait": avg_completed_wait,
    }


def service_coverage_pairs(counters):
    """Use itertools.combinations to find pairs sharing service capabilities."""
    rows = []
    for first, second in combinations(counters, 2):
        shared = set(first.supported_services).intersection(set(second.supported_services))
        if shared:
            rows.append((first.name, second.name, tuple(sorted(shared))))
    return rows


def simulate_load(incoming_service_times, counter_count):
    """Simulate shortest-workload routing and return average/max wait.

    This is a small educational simulation, not a real operations-research model.
    """
    if counter_count <= 0:
        return {"average_wait": 0.0, "maximum_wait": 0.0, "workloads": []}

    workloads = [0 for _ in range(counter_count)]
    waits = []

    for service_minutes in incoming_service_times:
        smallest_index = 0
        for index in range(1, len(workloads)):
            if workloads[index] < workloads[smallest_index]:
                smallest_index = index
        waits.append(workloads[smallest_index])
        workloads[smallest_index] += service_minutes

    wait_array = np.array(waits)
    workload_array = np.array(workloads)
    return {
        "average_wait": float(np.mean(wait_array)) if len(wait_array) else 0.0,
        "maximum_wait": float(np.max(wait_array)) if len(wait_array) else 0.0,
        "workloads": workload_array.tolist(),
    }


def compare_capacity_options(incoming_service_times, minimum_counters=1, maximum_counters=5):
    """Compare counter counts for a what-if analysis."""
    results = []
    for count in range(minimum_counters, maximum_counters + 1):
        result = simulate_load(incoming_service_times, count)
        results.append((count, result))
    return results


"""Demo data for FLOWIQ."""


SERVICES = (
    "Admissions",
    "Fees",
    "Documents",
    "IT Support",
    "Library",
    "Wellness",
)


def build_demo_center():
    center = FlowCenter()
    center.add_counter(ServiceCounter(1, "Front Desk", ("Admissions", "Fees", "Documents"), 6))
    center.add_counter(ServiceCounter(2, "Digital Help Desk", ("IT Support", "Admissions"), 4))
    center.add_counter(ServiceCounter(3, "Library Desk", ("Library", "Documents"), 5))
    center.add_counter(ServiceCounter(4, "Student Care", ("Wellness", "Fees"), 7))

    demo_people = [
        Student("Aarav", "26BCE1001"),
        Student("Diya", "26BCE1002"),
        Student("Kabir", "26BCE1003"),
        Student("Meera", "26BCE1004"),
        Student("Ishaan", "26BCE1005"),
        Student("Anaya", "26BCE1006"),
    ]

    requests = [
        ServiceRequest(demo_people[0], "Admissions", 6, 6),
        ServiceRequest(demo_people[1], "IT Support", 8, 5),
        ServiceRequest(demo_people[2], "Documents", 5, 7),
        UrgentRequest(demo_people[3], "Fees", 9, 8),
        ServiceRequest(demo_people[4], "Library", 4, 5),
        ServiceRequest(demo_people[5], "IT Support", 6, 6),
    ]

    for request in requests:
        center.add_request_record(request)
        assign_request(center.counters, request)

    # Create a small amount of wait-time diversity for analytics/demo.
    for request in center.pending_requests():
        request.waiting_minutes = (request.request_id - 1000) % 8

    for counter in center.counters:
        counter.queue.sort()

    return center


"""FLOWIQ - Smart Waiting, Booking & Service Flow Optimization System.

Run with:
    python main.py
"""



def print_title(title):
    print("\n" + "=" * 68)
    print(title.center(68))
    print("=" * 68)


def show_dashboard(center):
    stats = dashboard(center.counters, center.requests)
    print_title("FLOWIQ LIVE DASHBOARD")
    print(f"Service center          : {center.name}")
    print(f"Active counters         : {stats['active_counters']}")
    print(f"Customers waiting       : {stats['total_waiting']}")
    print(f"Total queued workload   : {stats['total_workload_minutes']} min")
    print(f"Average queue length    : {stats['average_queue']:.2f}")
    print(f"Maximum queue           : {stats['maximum_queue']}")
    print(f"Tickets served          : {stats['tickets_served']}")
    print(f"Avg wait of completed   : {stats['average_completed_wait']:.2f} min")

    print("\nCOUNTER LOAD")
    for counter in center.counters:
        print(
            f"C{counter.counter_id} | {counter.name:<20} | "
            f"queue={len(counter.queue):<2} | workload={counter.workload_minutes():<3} min | {counter.utilization_band()}"
        )


def show_queues(center):
    print_title("LIVE QUEUES")
    for counter in center.counters:
        print(f"\n{counter} | Supports: {', '.join(counter.supported_services)}")
        if not counter.queue:
            print("  (empty)")
        else:
            for position, request in enumerate(counter.queue, start=1):
                print(f"  {position}. {request.summary()}")


def read_int(prompt, minimum=None, maximum=None):
    while True:
        try:
            value = int(input(prompt).strip())
            if minimum is not None and value < minimum:
                print(f"Enter a value >= {minimum}.")
                continue
            if maximum is not None and value > maximum:
                print(f"Enter a value <= {maximum}.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number.")


def register_request(center):
    print_title("REGISTER NEW SERVICE REQUEST")
    name = input("Student/customer name: ").strip() or "Guest User"
    person_id = input("ID (e.g. 26BCE1010): ").strip() or "GUEST"
    student = Student(name, person_id)

    services = ["Admissions", "Fees", "Documents", "IT Support", "Library", "Wellness"]
    print("\nServices:")
    for number, service in enumerate(services, start=1):
        print(f"{number}. {service}")
    service_choice = read_int("Choose service: ", 1, len(services))
    service = services[service_choice - 1]

    urgency = read_int("Urgency (1-10): ", 1, 10)
    impact = read_int("Impact (1-10): ", 1, 10)
    group_size = read_int("People affected / group size: ", 1, 100)
    urgent = urgency >= 9

    if urgent:
        request = UrgentRequest(student, service, urgency, impact, group_size)
    else:
        request = ServiceRequest(student, service, urgency, impact, group_size)

    center.add_request_record(request)
    counter = assign_request(center.counters, request)
    if counter is None:
        request.status = "UNASSIGNED"
        print("\nNo active counter currently supports this service.")
        return

    wait = estimate_wait(counter)
    score, label = calculate_priority(request)
    print("\nREQUEST CREATED")
    print(f"Ticket ID             : {request.request_id}")
    print(f"Priority score        : {score:.1f} ({label})")
    print(f"Suggested counter     : {counter.name}")
    print(f"Estimated wait        : {wait} min")
    print("Reason                : Lowest projected workload among eligible counters.")


def recommend_counter(center):
    print_title("SMART COUNTER RECOMMENDATION")
    service = input("Service required: ").strip()
    urgency = read_int("Urgency (1-10): ", 1, 10)
    impact = read_int("Impact (1-10): ", 1, 10)
    group_size = read_int("People affected / group size: ", 1, 100)
    request = ServiceRequest(Student("Demo User", "DEMO"), service, urgency, impact, group_size)
    counter = smart_counter_recommendation(center.counters, request)

    if counter is None:
        print("No eligible counter found for this service.")
        return

    print(f"\nRecommended counter : {counter.name}")
    print(f"Current queue       : {len(counter.queue)}")
    print(f"Projected workload  : {counter.workload_minutes()} min")
    print(f"Estimated wait      : {estimate_wait(counter)} min")
    print("Reason              : Minimum workload first; queue length and speed break ties.")


def process_customer(center):
    print_title("PROCESS NEXT CUSTOMER")
    for counter in center.counters:
        print(f"C{counter.counter_id}. {counter.name} - {len(counter.queue)} waiting")
    counter_id = read_int("Counter number: ", 1)
    counter = center.find_counter(counter_id)
    if counter is None:
        print("Counter not found.")
        return
    completed = process_next(counter)
    if completed is None:
        print("This counter queue is empty.")
        return
    center.service_history.append(completed)
    print(f"Completed ticket #{completed.request_id} for {completed.person.name}.")


def what_if_simulation(center):
    print_title("WHAT-IF CAPACITY SIMULATION")
    print("This uses demo service durations to compare different counter counts.")
    raw = input("Enter service times in minutes (e.g. 4 5 6 4 7 5): ").strip()
    try:
        incoming = [int(value) for value in raw.split()]
    except ValueError:
        print("Use only whole numbers separated by spaces.")
        return
    if not incoming or any(value <= 0 for value in incoming):
        print("Enter at least one positive service time.")
        return

    results = compare_capacity_options(incoming, 1, min(6, len(incoming)))
    print("\nCOUNTER COUNT | AVG WAIT | MAX WAIT")
    for count, result in results:
        print(f"{count:^13} | {result['average_wait']:>8.2f} | {result['maximum_wait']:>8.2f}")


def capability_pairs(center):
    print_title("COUNTER CAPABILITY PAIRS")
    rows = service_coverage_pairs(center.counters)
    if not rows:
        print("No shared service capabilities found.")
        return
    for first, second, shared in rows:
        print(f"{first} <-> {second}")
        print(f"  Shared services: {', '.join(shared)}")


def demo_view(center):
    print_title("FLOWIQ DEMO SCENARIO")
    print("The demo starts with realistic sample requests routed to multiple counters.")
    show_dashboard(center)
    print("\nSMART ROUTING EXAMPLE")
    for counter in center.counters:
        print(f"{counter.name:<20} queue={len(counter.queue)} workload={counter.workload_minutes()} min")
    show_queues(center)


def main():
    center = build_demo_center()
    while True:
        print_title("FLOWIQ | SMART SERVICE FLOW ENGINE")
        print("1. Live dashboard")
        print("2. View queues")
        print("3. Register new request")
        print("4. Smart counter recommendation")
        print("5. Process next customer")
        print("6. Advance simulated time")
        print("7. What-if capacity simulation")
        print("8. Counter capability pairs")
        print("9. Run demo scenario")
        print("0. Exit")

        choice = input("\nChoose an option: ").strip()
        if choice == "1":
            show_dashboard(center)
        elif choice == "2":
            show_queues(center)
        elif choice == "3":
            register_request(center)
        elif choice == "4":
            recommend_counter(center)
        elif choice == "5":
            process_customer(center)
        elif choice == "6":
            minutes = read_int("Advance time by how many minutes? ", 1, 120)
            advance_time(center.counters, minutes)
            print(f"Added {minutes} simulated waiting minutes to queued requests.")
        elif choice == "7":
            what_if_simulation(center)
        elif choice == "8":
            capability_pairs(center)
        elif choice == "9":
            demo_view(center)
        elif choice == "0":
            print("Thank you for using FLOWIQ.")
            break
        else:
            print("Choose one of the displayed options.")


if __name__ == "__main__":
    main()
