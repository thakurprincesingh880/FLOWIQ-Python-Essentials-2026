"""Non-interactive FLOWIQ demonstration for evaluation/submission."""

from flowiq.analytics import dashboard, compare_capacity_options, service_coverage_pairs
from flowiq.engine import smart_counter_recommendation
from flowiq.models import ServiceRequest, Student
from flowiq.sample_data import build_demo_center


def main():
    center = build_demo_center()
    print("=" * 72)
    print("FLOWIQ - SMART SERVICE FLOW OPTIMIZATION SYSTEM")
    print("=" * 72)

    stats = dashboard(center.counters, center.requests)
    print("\nLIVE DASHBOARD")
    for key, value in stats.items():
        print(f"{key:24}: {value}")

    print("\nCOUNTER STATUS")
    for counter in center.counters:
        print(
            f"C{counter.counter_id} | {counter.name:<20} | "
            f"queue={len(counter.queue)} | workload={counter.workload_minutes()} min | {counter.utilization_band()}"
        )

    test_request = ServiceRequest(Student("Demo User", "DEMO"), "IT Support", 8, 7, 1)
    chosen = smart_counter_recommendation(center.counters, test_request)
    print("\nSMART ALLOCATION")
    print(f"Service requested : {test_request.service}")
    print(f"Recommended       : {chosen.name if chosen else 'No eligible counter'}")
    if chosen:
        print(f"Current queue     : {len(chosen.queue)}")
        print(f"Estimated wait    : {chosen.workload_minutes()} min")

    print("\nWHAT-IF SIMULATION")
    incoming = [4, 5, 7, 4, 6, 5, 8, 4]
    for count, result in compare_capacity_options(incoming, 1, 4):
        print(
            f"{count} counter(s): average wait={result['average_wait']:.2f} min, "
            f"maximum wait={result['maximum_wait']:.2f} min"
        )

    print("\nSHARED SERVICE CAPABILITIES")
    for first, second, shared in service_coverage_pairs(center.counters):
        print(f"{first} <-> {second}: {', '.join(shared)}")

    print("\nDEMO COMPLETE")


if __name__ == "__main__":
    main()
