"""Simple no-dependency self-test for FLOWIQ."""

from flowiq.analytics import dashboard, simulate_load
from flowiq.engine import assign_request, smart_counter_recommendation
from flowiq.models import ServiceCounter, ServiceRequest, Student
from flowiq.sample_data import build_demo_center


def run_tests():
    center = build_demo_center()
    assert len(center.counters) == 4
    assert center.total_pending() == 6

    request = ServiceRequest(Student("Test", "T01"), "IT Support", 6, 6, 1)
    counter = smart_counter_recommendation(center.counters, request)
    assert counter is not None
    assigned = assign_request(center.counters, request)
    assert assigned is counter
    assert request.assigned_counter == counter.name

    stats = dashboard(center.counters, center.requests)
    assert stats["active_counters"] == 4
    assert stats["total_waiting"] == 7

    simulation = simulate_load([4, 5, 6, 4, 5], 2)
    assert simulation["average_wait"] >= 0
    assert len(simulation["workloads"]) == 2

    print("ALL FLOWIQ SELF-TESTS PASSED")


if __name__ == "__main__":
    run_tests()
