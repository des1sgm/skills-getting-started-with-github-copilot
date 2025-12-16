import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

def test_signup_and_unregister():
    # Use a known activity and a test email
    activity_name = list(client.get("/activities").json().keys())[0]
    test_email = "pytestuser@example.com"

    # Ensure not already signed up
    client.delete(f"/activities/{activity_name}/unregister?email={test_email}")

    # Sign up
    signup = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert signup.status_code == 200
    assert f"Signed up {test_email}" in signup.json().get("message", "")

    # Try duplicate signup
    dup = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert dup.status_code == 400

    # Unregister
    unreg = client.delete(f"/activities/{activity_name}/unregister?email={test_email}")
    assert unreg.status_code == 200
    assert f"Unregistered {test_email}" in unreg.json().get("message", "")

    # Unregister again (should fail)
    unreg2 = client.delete(f"/activities/{activity_name}/unregister?email={test_email}")
    assert unreg2.status_code == 400
