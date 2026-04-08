def get_auth_token(client):
    # Try to register, ignore if already exists
    client.post(
        "/api/v1/auth/register",
        json={"name": "Book User", "email": "book@example.com", "password": "securepassword"}
    )
    # Login
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "book@example.com", "password": "securepassword"}
    )
    return resp.json()["access_token"]

def test_create_read_book(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create book
    create_resp = client.post(
        "/api/v1/books/",
        json={"title": "My Test Book", "description": "This is a test book", "is_public": True},
        headers=headers
    )
    assert create_resp.status_code == 200
    book_data = create_resp.json()
    assert book_data["title"] == "My Test Book"
    assert "id" in book_data
    book_id = book_data["id"]

    # Read book list
    list_resp = client.get("/api/v1/books/", headers=headers)
    assert list_resp.status_code == 200
    books = list_resp.json()
    assert len(books) > 0
    assert any(b["id"] == book_id for b in books)

    # Read specific book
    single_resp = client.get(f"/api/v1/books/{book_id}", headers=headers)
    assert single_resp.status_code == 200
    assert single_resp.json()["id"] == book_id

def test_unauthorized_access(client):
    list_resp = client.get("/api/v1/books/")
    assert list_resp.status_code == 401
