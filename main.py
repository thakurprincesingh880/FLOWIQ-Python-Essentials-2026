"""FLOWIQ - Smart Waiting, Booking & Service Flow Optimization System.

Run with:
    python main.py
"""

from flowiq.analytics import dashboard, compare_capacity_options, service_coverage_pairs
from flowiq.engine import assign_request, advance_time, calculate_priority, estimate_wait, process_next, smart_counter_recommendation
from flowiq.models import ServiceRequest, Student, UrgentRequest
from flowiq.sample_data import build_demo_center


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
