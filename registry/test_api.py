#!/usr/bin/env python3
"""
Simple test script to verify the Function Execution Service API.
Make sure the service is running before executing this script.
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


def test_api():
    """Test the complete API flow."""

    print("=" * 60)
    print("Testing Function Execution Service API")
    print("=" * 60)

    # 1. Register a user
    print("\n1. Registering user...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    if response.status_code == 201:
        print("✓ User registered successfully")
    elif response.status_code == 400:
        print("ℹ User already exists, continuing...")
    else:
        print(f"✗ Registration failed: {response.text}")
        return

    # 2. Login
    print("\n2. Logging in...")
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json=login_data
    )

    if response.status_code != 200:
        print(f"✗ Login failed: {response.text}")
        return

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✓ Login successful")

    # 3. Create a function
    print("\n3. Creating a function...")
    function_code = """def add_numbers(a, b):
    '''Add two numbers and return the result'''
    return a + b"""

    function_data = {
        "alias": "add_numbers",
        "code": function_code,
        "description": "Adds two numbers",
        "memory_limit_mb": 200,
        "timeout_seconds": 30
    }

    response = requests.post(
        f"{BASE_URL}/functions/",
        json=function_data,
        headers=headers
    )

    if response.status_code == 201:
        print("✓ Function created successfully")
        print(f"  Function ID: {response.json()['id']}")
    elif response.status_code == 400 and "already exists" in response.text:
        print("ℹ Function already exists, continuing...")
    else:
        print(f"✗ Function creation failed: {response.text}")
        return

    # 4. Execute the function
    print("\n4. Executing function...")
    execution_data = {
        "params": {
            "a": 10,
            "b": 25
        }
    }

    response = requests.post(
        f"{BASE_URL}/execute/add_numbers",
        json=execution_data,
        headers=headers
    )

    if response.status_code == 200:
        result = response.json()
        print("✓ Function executed successfully")
        print(f"  Result: {result['output']['result']}")
        print(f"  Execution time: {result['execution_time_ms']:.2f}ms")
        print(f"  Memory used: {result['memory_used_mb']:.2f}MB")
    else:
        print(f"✗ Function execution failed: {response.text}")
        return

    # 5. List functions
    print("\n5. Listing all functions...")
    response = requests.get(f"{BASE_URL}/functions/", headers=headers)

    if response.status_code == 200:
        functions = response.json()
        print(f"✓ Found {len(functions)} function(s)")
        for func in functions:
            print(f"  - {func['alias']}: {func['description']}")
    else:
        print(f"✗ Listing functions failed: {response.text}")

    # 6. Get execution history
    print("\n6. Getting execution history...")
    response = requests.get(
        f"{BASE_URL}/execute/history/add_numbers?limit=5",
        headers=headers
    )

    if response.status_code == 200:
        executions = response.json()
        print(f"✓ Found {len(executions)} execution(s)")
        for exec in executions[:3]:  # Show last 3
            print(f"  - Status: {exec['status']}, Time: {exec['execution_time_ms']:.2f}ms")
    else:
        print(f"✗ Getting execution history failed: {response.text}")

    # 7. Create a more complex function
    print("\n7. Creating a complex function...")
    complex_code = """def fibonacci(n):
    '''Calculate the nth Fibonacci number'''
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b"""

    function_data = {
        "alias": "fibonacci",
        "code": complex_code,
        "description": "Calculates nth Fibonacci number",
        "memory_limit_mb": 150,
        "timeout_seconds": 10
    }

    response = requests.post(
        f"{BASE_URL}/functions/",
        json=function_data,
        headers=headers
    )

    if response.status_code == 201:
        print("✓ Complex function created successfully")
    elif response.status_code == 400 and "already exists" in response.text:
        print("ℹ Function already exists, continuing...")
    else:
        print(f"✗ Complex function creation failed: {response.text}")

    # 8. Execute complex function
    print("\n8. Executing complex function...")
    execution_data = {"params": {"n": 20}}

    response = requests.post(
        f"{BASE_URL}/execute/fibonacci",
        json=execution_data,
        headers=headers
    )

    if response.status_code == 200:
        result = response.json()
        print("✓ Complex function executed successfully")
        print(f"  Fibonacci(20) = {result['output']['result']}")
        print(f"  Execution time: {result['execution_time_ms']:.2f}ms")
    else:
        print(f"✗ Complex function execution failed: {response.text}")

    # 9. Test timeout
    print("\n9. Testing timeout...")
    timeout_code = """def slow_function():
    '''This function will timeout'''
    import time
    time.sleep(100)  # Sleep for 100 seconds
    return 'completed'"""

    function_data = {
        "alias": "slow_function",
        "code": timeout_code,
        "description": "A function that will timeout",
        "timeout_seconds": 2
    }

    # Create the function
    response = requests.post(
        f"{BASE_URL}/functions/",
        json=function_data,
        headers=headers
    )

    if response.status_code in [201, 400]:
        # Execute it
        response = requests.post(
            f"{BASE_URL}/execute/slow_function",
            json={"params": {}},
            headers=headers
        )

        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'timeout':
                print("✓ Timeout handling works correctly")
                print(f"  Error: {result['error_message']}")
            else:
                print("✗ Expected timeout but got: " + result['status'])
        else:
            print(f"✗ Timeout test failed: {response.text}")

    print("\n" + "=" * 60)
    print("API Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to API at " + BASE_URL)
        print("  Make sure the service is running:")
        print("  - With Docker: docker-compose up")
        print("  - Local: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
