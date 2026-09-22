"""
Standalone Python Load & Concurrency Benchmark Runner for ChargeWise AI.
Simulates concurrent user load (10, 50, 100 users) and computes latency percentiles (p50, p90, p95, p99).
"""
import time
import requests
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from tabulate import tabulate
import argparse
import json


def benchmark_endpoint(url: str, method: str = "GET", payload: dict = None, concurrency: int = 20, total_requests: int = 100):
    """Executes concurrent load test against target URL."""
    latencies = []
    status_counts = {}
    
    start_wall_time = time.time()

    def send_single_request():
        req_start = time.time()
        try:
            if method.upper() == "POST":
                res = requests.post(url, json=payload, timeout=10)
            else:
                res = requests.get(url, timeout=10)
            elapsed_ms = (time.time() - req_start) * 1000
            return res.status_code, elapsed_ms
        except Exception as e:
            return 500, (time.time() - req_start) * 1000

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(send_single_request) for _ in range(total_requests)]
        for f in as_completed(futures):
            status, latency = f.result()
            latencies.append(latency)
            status_counts[status] = status_counts.get(status, 0) + 1

    total_time = time.time() - start_wall_time
    throughput = len(latencies) / total_time if total_time > 0 else 0

    return {
        "concurrency": concurrency,
        "total_requests": total_requests,
        "throughput_rps": round(throughput, 2),
        "min_ms": round(min(latencies), 2) if latencies else 0,
        "avg_ms": round(statistics.mean(latencies), 2) if latencies else 0,
        "p50_ms": round(statistics.median(latencies), 2) if latencies else 0,
        "p90_ms": round(statistics.quantiles(latencies, n=10)[8], 2) if len(latencies) >= 10 else 0,
        "p95_ms": round(statistics.quantiles(latencies, n=20)[18], 2) if len(latencies) >= 20 else 0,
        "status_distribution": status_counts
    }


def run_full_benchmark():
    print("=================================================================")
    print("      ChargeWise AI - Automated Performance Load Benchmark       ")
    print("=================================================================")

    endpoints = [
        {
            "name": "Station Discovery (/api/v1/stations/nearby)",
            "url": "http://localhost:8080/api/v1/stations/nearby?lat=13.0418&lng=80.2341&radiusKm=50",
            "method": "GET",
            "payload": None
        },
        {
            "name": "Slot Reservation (/api/v1/bookings/reserve)",
            "url": "http://localhost:8080/api/v1/bookings/reserve",
            "method": "POST",
            "payload": {"stationId": "st-001", "userPhone": "+91 98765 43210", "vehicleType": "EV Fleet Cab", "paymentMethod": "UPI"}
        },
        {
            "name": "ML Wait Time Predictor (:8000/predict/waiting-time)",
            "url": "http://localhost:8000/predict/waiting-time",
            "method": "POST",
            "payload": {"day_of_week": 2, "hour_of_day": 14, "total_chargers": 6, "current_occupancy": 4}
        }
    ]

    tier_concurrencies = [10, 50, 100]
    summary_rows = []

    for ep in endpoints:
        print(f"\nEvaluating Endpoint: {ep['name']}...")
        for c in tier_concurrencies:
            res = benchmark_endpoint(
                url=ep["url"],
                method=ep["method"],
                payload=ep["payload"],
                concurrency=c,
                total_requests=c * 5
            )
            summary_rows.append([
                ep["name"][:25],
                c,
                res["total_requests"],
                f"{res['throughput_rps']} rps",
                f"{res['avg_ms']} ms",
                f"{res['p95_ms']} ms",
                str(res["status_distribution"])
            ])

    headers = ["Endpoint", "Virtual Users", "Total Req", "Throughput", "Avg Latency", "p95 Latency", "Status Codes"]
    print("\n" + tabulate(summary_rows, headers=headers, tablefmt="fancy_grid"))


if __name__ == "__main__":
    run_full_benchmark()
