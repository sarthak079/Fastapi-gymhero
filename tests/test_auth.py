def test_create_user(client):
    response=client.post(
        "/users/",
        json={"name":"Test User","email":"test@example.com","password":"testpassword"}
    )
    # --- ADD THIS DEBUGGING BLOCK ---
    if response.status_code != 200:
        print("\nDEBUGGING 422 ERROR:")
        print(response.json())  # This will print exactly what field is missing!
    
    assert response.status_code==200
    data=response.json()
    assert data["email"]=="test@example.com"
    assert "id" in data
    assert "password" not in data
    
def test_login_and_get_token(client):
    # First, create a user
    client.post(
        "/users/",
        json={"name":"Login User","email":"login@example.com","password":"loginpassword"}
    )

    response=client.post(
        "/token",
        data={"username":"Login User","password":"loginpassword"}
    )
    assert response.status_code==200
    data=response.json()
    assert "access_token" in data
    assert data["token_type"]=="bearer"