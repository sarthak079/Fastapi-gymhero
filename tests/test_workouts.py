def test_create_workout(client):
    client.post("/users/",json={"name":"Workout User","email":"workout@example.com","password":"workoutpassword"})
    login_res=client.post("/token", data={"username":"Workout User","password":"workoutpassword"})
    token=login_res.json()["access_token"]

    headers={"Authorization":f"Bearer {token}"}

    workout_data={
        "name":"Morning Routine",
        "description":"A quick morning workout",
        "date":"2024-01-01"
    }

    response=client.post("/workouts/", json=workout_data, headers=headers)
    assert response.status_code==200
    data=response.json()
    assert data["name"]=="Morning Routine"
    assert data["hero_id"] is not None