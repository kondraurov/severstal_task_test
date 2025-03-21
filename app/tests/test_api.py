from fastapi.testclient import TestClient
from main import app
from app.rolls.schemas import SchemasRoll
from datetime import date

client = TestClient(app)

def test_add_roll():
    roll_data = SchemasRoll(
        length=10.0,
        weight=20.0,
        date_added=date(2025, 3, 1),
        date_removed=date(2025, 3, 10)
    )
    response = client.post("/roll/add", json=roll_data.model_dump())
    assert response.status_code == 200
    assert response.json()["length"] == 10.0
    assert response.json()["weight"] == 20.0

def test_delete_roll():
    roll_data = SchemasRoll(
        length=10.0,
        weight=20.0,
        date_added=date(2025, 3, 1),
        date_removed=date(2025, 3, 10)
    )
    add_response = client.post("/roll/add", json=roll_data.model_dump())
    assert add_response.status_code == 200
    roll_id = add_response.json()["id"]

    delete_response = client.delete(f"/roll/delete/{roll_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == roll_id

    get_response = client.get(f"/roll/{roll_id}")
    assert get_response.status_code == 404

def test_get_all_rolls():
    rolls = [
        SchemasRoll(length=10.0, weight=20.0, date_added=date(2025, 3, 1), date_removed=date(2025, 3, 10)),
        SchemasRoll(length=30.0, weight=40.0, date_added=date(2025, 3, 5), date_removed=date(2025, 3, 15))
    ]
    for roll in rolls:
        client.post("/roll/add", json=roll.model_dump())

    response = client.get("/roll/all")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2

def test_filter_rolls():
    rolls = [
        SchemasRoll(length=10.0, weight=20.0, date_added=date(2025, 3, 1), date_removed=date(2025, 3, 10)),
        SchemasRoll(length=30.0, weight=40.0, date_added=date(2025, 3, 5), date_removed=date(2025, 3, 15))
    ]
    for roll in rolls:
        client.post("/roll/add", json=roll.model_dump())

    response = client.get("/roll/filter?min_weight=20&max_weight=30")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["weight"] == 20.0

def test_get_roll_stats():
    rolls = [
        SchemasRoll(length=10.0, weight=20.0, date_added=date(2025, 3, 1), date_removed=date(2025, 3, 10)),
        SchemasRoll(length=30.0, weight=40.0, date_added=date(2025, 3, 5), date_removed=date(2025, 3, 15))
    ]
    for roll in rolls:
        client.post("/roll/add", json=roll.model_dump())

    response = client.get("/roll/rolls/stats?start_date=2025-03-01&end_date=2025-03-15")
    assert response.status_code == 200
    data = response.json()
    assert "total_weight" in data
    assert "average_length" in data
    assert data["total_weight"] == 60.0  # 20 + 40
    assert data["average_length"] == 20.0  # (10 + 30) / 2