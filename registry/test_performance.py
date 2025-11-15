#!/usr/bin/env python3
"""
Performance test for the Function Execution Service.
Tests parallel execution with 1,000 concurrent requests.
"""

import asyncio
import time
import httpx
from statistics import mean, median, stdev

BASE_URL = "http://localhost:8000"


async def login():
    """Login and get access token."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/auth/login",
            json={"username": "testuser", "password": "testpassword123"}
        )
        if response.status_code != 200:
            raise Exception(f"Login failed: {response.text}")
        return response.json()["access_token"]


async def execute_function(client, token, request_id, a, b):
    """Execute the add_numbers function."""
    start_time = time.time()
    try:
        response = await client.post(
            f"{BASE_URL}/execute/add_numbers",
            json={"params": {"a": a, "b": b}},
            headers={"Authorization": f"Bearer {token}"}
        )
        elapsed = (time.time() - start_time) * 1000  # Convert to ms

        if response.status_code == 200:
            result = response.json()
            return {
                "request_id": request_id,
                "status": "success",
                "result": result["output"]["result"],
                "execution_time_ms": result.get("execution_time_ms", 0),
                "total_time_ms": elapsed,
                "status_code": response.status_code
            }
        else:
            return {
                "request_id": request_id,
                "status": "error",
                "error": response.text,
                "total_time_ms": elapsed,
                "status_code": response.status_code
            }
    except Exception as e:
        elapsed = (time.time() - start_time) * 1000
        return {
            "request_id": request_id,
            "status": "exception",
            "error": str(e),
            "total_time_ms": elapsed,
            "status_code": None
        }


async def run_performance_test(num_requests=1000, concurrency=50):
    """Run performance test with specified number of requests."""
    print("=" * 70)
    print(f"Performance Test: {num_requests} requests")
    print("=" * 70)

    # Login
    print("\n1. Logging in...")
    token = await login()
    print("✓ Login successful")

    # Prepare requests
    print(f"\n2. Preparing {num_requests} requests with concurrency of {concurrency}...")

    # Create semaphore to limit concurrency
    semaphore = asyncio.Semaphore(concurrency)

    async def bounded_execute(client, token, request_id, a, b):
        async with semaphore:
            return await execute_function(client, token, request_id, a, b)

    # Execute requests
    print(f"\n3. Executing {num_requests} parallel requests...")
    start_time = time.time()

    async with httpx.AsyncClient(timeout=60.0) as client:
        tasks = [
            bounded_execute(client, token, i, i, i+1)
            for i in range(num_requests)
        ]
        results = await asyncio.gather(*tasks)

    total_time = time.time() - start_time

    # Analyze results
    print("\n4. Analyzing results...")

    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] != "success"]

    total_times = [r["total_time_ms"] for r in results]
    exec_times = [r["execution_time_ms"] for r in successful]

    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    print(f"\n📊 Overall Performance:")
    print(f"  Total requests:        {num_requests}")
    print(f"  Successful:            {len(successful)} ({len(successful)/num_requests*100:.1f}%)")
    print(f"  Failed:                {len(failed)} ({len(failed)/num_requests*100:.1f}%)")
    print(f"  Total time:            {total_time:.2f}s")
    print(f"  Requests/second:       {num_requests/total_time:.2f}")

    print(f"\n⏱️  Response Time (Total - includes network + queue + execution):")
    print(f"  Mean:                  {mean(total_times):.2f}ms")
    print(f"  Median:                {median(total_times):.2f}ms")
    print(f"  Min:                   {min(total_times):.2f}ms")
    print(f"  Max:                   {max(total_times):.2f}ms")
    if len(total_times) > 1:
        print(f"  Std Dev:               {stdev(total_times):.2f}ms")

    if exec_times:
        print(f"\n⚡ Function Execution Time (Pure execution):")
        print(f"  Mean:                  {mean(exec_times):.2f}ms")
        print(f"  Median:                {median(exec_times):.2f}ms")
        print(f"  Min:                   {min(exec_times):.2f}ms")
        print(f"  Max:                   {max(exec_times):.2f}ms")
        if len(exec_times) > 1:
            print(f"  Std Dev:               {stdev(exec_times):.2f}ms")

    # Show errors if any
    if failed:
        print(f"\n❌ Failed Requests ({len(failed)}):")
        error_types = {}
        for r in failed:
            error_key = r.get("status_code", "exception")
            error_types[error_key] = error_types.get(error_key, 0) + 1

        for error_type, count in error_types.items():
            print(f"  {error_type}: {count}")

        # Show first few errors
        print("\n  First 5 errors:")
        for r in failed[:5]:
            print(f"    Request {r['request_id']}: {r.get('error', 'Unknown error')[:100]}")

    # Percentiles
    sorted_times = sorted(total_times)
    p50 = sorted_times[int(len(sorted_times) * 0.50)]
    p95 = sorted_times[int(len(sorted_times) * 0.95)]
    p99 = sorted_times[int(len(sorted_times) * 0.99)]

    print(f"\n📈 Percentiles (Response Time):")
    print(f"  p50 (median):          {p50:.2f}ms")
    print(f"  p95:                   {p95:.2f}ms")
    print(f"  p99:                   {p99:.2f}ms")

    print("\n" + "=" * 70)
    print("Test Complete!")
    print("=" * 70)


if __name__ == "__main__":
    import sys

    # Parse arguments
    num_requests = 1000
    concurrency = 50

    if len(sys.argv) > 1:
        num_requests = int(sys.argv[1])
    if len(sys.argv) > 2:
        concurrency = int(sys.argv[2])

    print(f"Running with {num_requests} requests and {concurrency} concurrent workers")

    asyncio.run(run_performance_test(num_requests, concurrency))
