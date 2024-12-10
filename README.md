# EventsAPI

## Prerequisites
- Docker
- Python 3.13
- Pipenv

---

## Project Setup

1. **Clone the repository**  
    ```
    git clone https://github.com/NathanJMF/EventsAPI.git
    cd EventsAPI
    ```

2. **Create a `.env` file** in the root of the project directory with the following structure:  
    ```
    GLOBAL_TEST_FLAG=true
    BACKEND_PORT=5000
    DB_HOST=your_db_host
    DB_PORT=your_db_port
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    ```

3. **Start the PostgreSQL database**  
    Make sure the Docker Engine is running, then use the provided `docker-compose.yml` file to spin up the database:  
    ```
    docker-compose up -d
    ```

4. **Set up the virtual environment using Pipenv**  
    ```
    pipenv shell
    pipenv sync
    ```

5. **Run Alembic migrations to set up the database structure**
    ```
    alembic upgrade head
    ```

6. **Add a user entry to the database manually**  
    Since the `/api/events` endpoint assumes the `user_id` exists in the database, you'll need to insert a user record into the `users` table manually. This can be done using a database client or a simple SQL command like:
    ```sql
    INSERT INTO users (user_id) VALUES (1);
    ```

7. **Start the API**  
    ```
    python app.py
    ```

The API will now be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).  
If you're using macOS, and port 5000 is already in use, consider setting `BACKEND_PORT=5001` in the `.env` file and accessing the API at [http://127.0.0.1:5001](http://127.0.0.1:5001).

---

## API Endpoints

- **Create Event**  
  - **POST** `/api/events`  
  - Request JSON Body:  
    ```json
    {
      "type": "deposit",
      "amount": "42.00",
      "user_id": 1,
      "time": 10
    }
    ```
  - Response:  
    ```json
    {
      "alert": true,
      "alert_codes": [123],
      "user_id": 1
    }
    ```

---

## System Overview

### Core Components
#### `config_loader.py`
Manages environment-specific configurations using a `.env` file, including database credentials and application flags.

#### `app.py`
Initializes the Flask application and sets up the primary `/api/events` endpoint.

#### `routes/events/resources.py`
Defines the logic for processing user actions (`deposit` or `withdraw`) and returns appropriate responses based on alert rules.

#### `routes/events/helpers.py`
Contains functions for evaluating alert conditions and performing database operations like user validation and action tracking.

---

### Database System
#### `models.py`
Defines the database schema for the `users`, `user_actions`, and `alerts` tables using SQLAlchemy.

#### `core.py`
Implements core database utilities for CRUD operations, including query execution, record insertion, updates, and deletions.

#### `alembic` (Migrations)
Automates schema changes using Alembic. Run migrations with:
```alembic upgrade head```

---

### Alerts
The system checks user actions against the following predefined rules:
- **Code: 1100** - Withdrawal amount exceeds 100.
- **Code: 30** - User makes 3 consecutive withdrawals.
- **Code: 300** - User makes 3 consecutive deposits, each larger than the last.
- **Code: 123** - Total deposits in a 30-second window exceed 200.

---

## Challenges

1. **Deviation from Task Simplicity**  
   - The task description did not explicitly require the use of a database, suggesting that an in-memory implementation might suffice. However, I opted for a more robust database-backed solution to ensure scalability and persistence. This choice added complexity, such as the need for database setup, manual user creation, and dependency management, which might not align with the task's intent to test basic functionality.

2. **Requirement for Pre-existing Users**  
   - The system requires that the `user_id` exists in the database before processing actions, responding with a ```404``` if the user does not exist. While this ensures data integrity, it introduces a dependency that is not explicitly required in the task. For simplicity, an alternative could have been to dynamically create users when an unknown `user_id` is encountered.

3. **Timestamp in the Request**  
   - The task specifies that the `timestamp` should be provided in the request body, which introduces potential risks, such as manipulation or abuse of the system by providing incorrect timestamps. If I were designing this API for production use, I would calculate the timestamp on the server side at the time the request is received to ensure data integrity and prevent abuse. However, I followed the directions given in the task to include the `timestamp` in the request as specified in the documentation.
