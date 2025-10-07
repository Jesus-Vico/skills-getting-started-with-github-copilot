import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

# Test get activities
def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

# Test signup for activity
@pytest.mark.parametrize("activity,email", [
    ("Chess Club", "newstudent@mergington.edu"),
    ("Programming Class", "another@mergington.edu")
])
def test_signup_for_activity(activity, email):
    # Remove if already present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in activities[activity]["participants"]

# Test duplicate signup
def test_signup_duplicate():
    activity = "Chess Club"
    email = "michael@mergington.edu"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"

# Test remove participant
def test_remove_participant():
    activity = "Chess Club"
    email = "daniel@mergington.edu"
    # Ensure present
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)
    response = client.post(f"/activities/{activity}/remove?email={email}")
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]

# Test remove non-existent participant
def test_remove_nonexistent():
    activity = "Chess Club"
    email = "notfound@mergington.edu"
    response = client.post(f"/activities/{activity}/remove?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered"

# Test signup for non-existent activity
def test_signup_nonexistent_activity():
    response = client.post("/activities/Unknown/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

# Test remove for non-existent activity
def test_remove_nonexistent_activity():
    response = client.post("/activities/Unknown/remove?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
