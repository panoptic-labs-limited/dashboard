#!/usr/bin/env python3
import httpx
import json

# Login
response = httpx.post(
    "http://localhost:8000/auth/login",
    json={"username": "testuser", "password": "testpassword123"}
)
token = response.json()["access_token"]

# Get dashboard
response = httpx.get(
    "http://localhost:8000/dashboards/plotly_datasets",
    headers={"Authorization": f"Bearer {token}"}
)

dashboard = response.json()

# Print first page structure to see input placement
page = dashboard["structure"]["children"][0]
print(f"Page: {page['title']}")
print(f"Page has {len(page['children'])} children")

def print_node(node, indent=0):
    prefix = "  " * indent
    if node['type'] == 'input':
        print(f"{prefix}- input: {node.get('input_type', 'unknown')} ({node.get('name', 'N/A')})")
    elif node['type'] == 'widget':
        print(f"{prefix}- widget: {node.get('title', 'N/A')}")
    else:
        title = node.get('title', node.get('id', 'N/A'))
        print(f"{prefix}- {node['type']}: {title}")

    if 'children' in node:
        for child in node['children']:
            print_node(child, indent + 1)

for i, child in enumerate(page['children']):
    print(f"\n{i+1}. Section: {child.get('title', 'N/A')}")
    if 'children' in child:
        for subchild in child['children']:
            print_node(subchild, 1)
