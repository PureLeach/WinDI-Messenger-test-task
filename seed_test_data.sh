#!/bin/bash

DB_HOST="localhost"

# Loading variables from .env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "❌ File .env not found!"
  exit 1
fi

# Checking if psql is installed
if ! command -v psql &> /dev/null; then
    echo "❌ Error: psql not found! Install the PostgreSQL client."
    exit 1
fi

# Exporting the password for psql
export PGPASSWORD=$POSTGRES_PASSWORD

# Executing SQL queries
psql -h $DB_HOST -p $POSTGRES_PORT -d $POSTGRES_DB_NAME -U $POSTGRES_USER <<EOF

-- Data cleanup
TRUNCATE TABLE group_participants, messages, chats, users RESTART IDENTITY CASCADE;

-- We insert users and save their IDs
WITH inserted_users AS (
    INSERT INTO users (id, name, email, password)
    VALUES
        (gen_random_uuid(), 'Alice', 'alice@example.com', 'hashed_password'),
        (gen_random_uuid(), 'Bob', 'bob@example.com', 'hashed_password'),
        (gen_random_uuid(), 'Charlie', 'charlie@example.com', 'hashed_password')
    RETURNING id, email
)
SELECT * FROM inserted_users;

-- Inserting chats
WITH inserted_chats AS (
    INSERT INTO chats (id, name, type)
    VALUES
        (gen_random_uuid(), 'Group Chat', 'group'),
        (gen_random_uuid(), 'Personal Chat', 'personal')
    RETURNING id, name
)
SELECT * FROM inserted_chats;

-- Inserting the group chat participants
INSERT INTO group_participants (chat_id, user_id)
SELECT c.id, u.id
FROM users u
CROSS JOIN chats c
WHERE c.name = 'Group Chat' AND u.email IN ('alice@example.com', 'bob@example.com', 'charlie@example.com');

-- Inserting messages
INSERT INTO messages (id, chat_id, sender_id, text, created_at, updated_at, read)
SELECT gen_random_uuid(), c.id, u.id, 
       CASE u.email
           WHEN 'alice@example.com' THEN 'Hi guys!'
           WHEN 'bob@example.com' THEN 'Hello, Alice.!'
           WHEN 'charlie@example.com' THEN 'Hello, are you there??'
       END,
       now(), now(), false
FROM users u
CROSS JOIN chats c
WHERE (c.name = 'Group Chat' AND u.email IN ('alice@example.com', 'bob@example.com'))
   OR (c.name = 'Personal Chat' AND u.email = 'charlie@example.com');

EOF

echo "✅ Messenger database has been successfully filled with test data."
