#!/usr/bin/env python3
"""Test component registration to see detailed error messages."""

import httpx
from viz.api.serializer import serialize_component
from examples.plotly_datasets_dashboard import GapminderTrends

# Login
client = httpx.Client()
response = client.post(
    "http://localhost:8000/auth/login",
    json={"username": "testuser", "password": "testpassword123"}
)
response.raise_for_status()
token = response.json()["access_token"]

# Serialize component
component_data = serialize_component(GapminderTrends, "gapminder_trends")

print("Component data:")
import json
print(json.dumps(component_data, indent=2))

# Try to register
response = client.post(
    "http://localhost:8000/components/",
    json=component_data,
    headers={"Authorization": f"Bearer {token}"}
)

print(f"\nStatus: {response.status_code}")
print(f"Response: {response.text}")
