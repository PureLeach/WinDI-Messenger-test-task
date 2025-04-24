# Messenger test task

A mini messenger application with the ability to send messages, store them in a database, and create group chats. Completed as part of a test assignment for the position of Backend developer.

---

## 📦 Functionality

- Connection via WebSocket
- Real-time text messaging
- Storing messages in PostgreSQL
- Tracking the reading of messages
- A REST endpoint for getting the message history
- Prevent duplicate messages when sending in parallel
- Swagger documentation
- Containerization with Docker

---

## Quick Start

1. Copy the example environment file:

   ```bash
   cp example.env .env
   ```
2. Build the Docker containers:

   ```bash
   docker-compose build
   ```
3. Start the app:

   ```bash
   docker-compose up
   ```

---

## Interfaces

- Swagger UI: http://localhost:8000/docs
- pgAdmin: http://localhost:5050

---

## API Documentation

### Users

#### Create User

- **Endpoint:** `POST /users/`
- **Description:** Creates a new user.
- **Request Body (application/json):**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

- **Response (200 OK):**

```json
{
  "id": "uuid",
  "name": "John Doe",
  "email": "john@example.com"
}
```

### Chats

#### Create Chat

- **Endpoint:** `POST /chats/`
- **Description:** Creates a new chat.
- **Request Body (application/json):**

```json
{
  "name": "Work Chat",
  "type": "group",
  "participantIds": ["uuid1", "uuid2"]
}
```

- **Response (200 OK):**

```json
{
  "id": "uuid",
  "name": "Work Chat",
  "type": "group",
  "participantIds": ["uuid1", "uuid2"]
}
```

#### Get Chats for User

- **Endpoint:** `GET /chats/?user_id=uuid`
- **Description:** Retrieves all chats the user is a part of.
- **Response (200 OK):**

```json
[
  {
    "id": "uuid",
    "name": "Work Chat",
    "type": "group",
    "participantIds": ["uuid1", "uuid2"]
  }
]
```

#### Add User to Chat

- **Endpoint:** `POST /chats/{chat_id}/users/{user_id}`
- **Description:** Adds a user to the specified chat.
- **Response (200 OK):**

```json
{
  "id": "uuid",
  "name": "Work Chat",
  "type": "group",
  "participantIds": ["uuid1", "uuid2", "uuid3"]
}
```

### Messages

#### Get Message History

- **Endpoint:** `GET /messages/history/{chat_id}`
- **Description:** Retrieves the message history for a given chat.
- **Query Parameters (optional):**
  - `limit`: Number of messages to return (default: 100)
  - `offset`: Pagination offset (default: 0)
- **Response (200 OK):**

```json
[
  {
    "id": "uuid",
    "chatId": "uuid",
    "senderId": "uuid",
    "text": "Hello!",
    "read": true,
    "createdAt": "2025-04-24T12:00:00Z",
    "updatedAt": "2025-04-24T12:00:00Z"
  }
]
```

---

### WebSocket

#### Chat Messaging

- **Endpoint:** `ws://localhost:8000/messages/ws/{chat_id}/{user_id}`
- **Description:** Opens a real-time WebSocket connection for sending and receiving messages in a chat.

#### Message Types

1. **Send a Message**

   - Sends a new chat message to all participants.
   - **Message Format:**
     ```json
     {
       "event": "message",
       "data": {
         "text": "Hey, how are you?"
       }
     }
     ```
2. **Mark as Read**

   - Notifies the server that a message has been read.
   - **Message Format:**
     ```json
     {
       "event": "read",
       "data": {
         "message_id": "f2abadb9-6a60-44c4-8c74-01aa2f520bf8"
       }
     }
     ```

---

## Tests:

To run the tests, load the dependencies using the pipenv package manager and run the command `> pytest`

1. Copy the sample environment file if you haven't done this before:

   ```bash
   cp example.env .env
   ```
2. Create a new virtual environment and install dependencies:

   ```bash
   pipenv shell
   pipenv install --dev
   ```
3. Start the postgres container:

   ```bash
   docker-compose up postgres
   ```
4. To run the project's tests, you can execute `pytest` from the root directory:

   ```bash
   pytest
   ```

---

## Technologies Used

- **FastAPI**: Fast web framework for building APIs with Python.
- **SQLAlchemy 2 (Async)**: ORM for Python with async support.
- **Databases**: Asynchronous database query library.
- **PostgreSQL**: Relational database management system used for storage.
- **Docker**: To run the project in a container.
- **Docker Compose**: To define and manage multi-container Docker applications.
- **Pipenv**: To manage project dependencies.

---
