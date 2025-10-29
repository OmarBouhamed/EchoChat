# Location: tests/test_conversations.py
import pytest


@pytest.mark.asyncio
async def test_create_conversation(client):
    """Test creating a new conversation."""
    payload = {"title": "Test Conversation"}
    response = await client.post("/v1/conversations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Conversation"
    assert "id" in data
    assert "user_id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_conversation(client):
    """Test getting a conversation."""
    # Create conversation first
    create_response = await client.post(
        "/v1/conversations",
        json={"title": "Test"}
    )
    conv_id = create_response.json()["id"]
    
    # Get it
    response = await client.get(f"/v1/conversations/{conv_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == conv_id


@pytest.mark.asyncio
async def test_add_message(client):
    """Test adding a message to conversation."""
    # Create conversation
    create_response = await client.post(
        "/v1/conversations",
        json={"title": "Test"}
    )
    conv_id = create_response.json()["id"]
    
    # Add message
    payload = {"content": "Hello, chatbot!"}
    response = await client.post(
        f"/v1/conversations/{conv_id}/messages",
        json=payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Hello, chatbot!"
    assert data["role"] == "user"
    assert data["conversation_id"] == conv_id


@pytest.mark.asyncio
async def test_get_messages(client):
    """Test getting messages from conversation."""
    # Create conversation
    create_response = await client.post(
        "/v1/conversations",
        json={"title": "Test"}
    )
    conv_id = create_response.json()["id"]
    
    # Add multiple messages
    for i in range(3):
        await client.post(
            f"/v1/conversations/{conv_id}/messages",
            json={"content": f"Message {i}"}
        )
    
    # Get messages
    response = await client.get(f"/v1/conversations/{conv_id}/messages")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_delete_conversation(client):
    """Test deleting a conversation."""
    # Create conversation
    create_response = await client.post(
        "/v1/conversations",
        json={"title": "Test"}
    )
    conv_id = create_response.json()["id"]
    
    # Delete it
    response = await client.delete(f"/v1/conversations/{conv_id}")
    assert response.status_code == 200
    
    # Verify it's gone
    response = await client.get(f"/v1/conversations/{conv_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_conversation_not_found(client):
    """Test getting non-existent conversation."""
    response = await client.get("/v1/conversations/fake-id-123")
    assert response.status_code == 404
