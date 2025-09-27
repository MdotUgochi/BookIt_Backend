Perfect 👍 Thanks for clarifying. I’ll rewrite the **README for BookIt API** in that *exact same format* (Features → Technologies Used → API Endpoints in a table).

---

# 📘 BookIt API

## Features

Authentication:

User registration, login, token refresh, and logout.
Secure JWT (JSON Web Token) authentication for access control.

User Management:

* Retrieve, update, and delete authenticated user accounts.
* Admin-only endpoints for managing users.

Service Management:

* CRUD operations for services (create, retrieve, update, delete).

Booking Management:

* Manage bookings for available services.

Reviews:

* Users can create, view, update, and delete reviews for services.

Swagger / FastAPI Integration:

* Auto-generated API documentation with **Swagger UI** and **ReDoc**.
* Clear, accessible documentation for developers to understand and test the API.

---

## Technologies Used

* FastAPI → High-performance Python web framework for building APIs. Chosen for its speed, type hint support, and built-in OpenAPI documentation.


* PostgreSQL → Relational database used for persistent data storage. (chosen for scalability and strong relational support).
* 
* SQLAlchemy → ORM for managing database models and queries.
* Alembic → Database migrations and schema versioning.
* JWT Authentication** → Token-based authentication (access + refresh tokens).
* Pydantic → Data validation and serialization.
* Uvicorn → ASGI server for running FastAPI applications in development/production.

---

## API Endpoints

| Endpoint                   | HTTP Method | Path                    | Description                                | User Type |
| -------------------------- | ----------- | ----------------------- | ------------------------------------------ | --------- |
| **Auth - Register**        | POST        | `/auth/register`        | Register a new user                        | User      |
| **Auth - Login**           | POST        | `/auth/login`           | Authenticate and generate access tokens    | User      |
| **Auth - Refresh**         | POST        | `/auth/refresh`         | Refresh access token using a refresh token | User      |
| **Auth - Logout**          | POST        | `/auth/logout`          | Revoke a refresh token and log out         | User      |
| **Get My Profile**         | GET         | `/users/me`             | Get authenticated user profile             | User      |
| **Update My Profile**      | PATCH       | `/users/me`             | Update authenticated user profile          | User      |
| **List Services**          | GET         | `/services/`            | Get all services                           | User      |
| **Create Service**         | POST        | `/services/`            | Create a new service                       | Admin     |
| **Retrieve Service by ID** | GET         | `/services/{id}`        | Get details of a specific service          | User      |
| **Update Service by ID**   | PUT         | `/services/{id}`        | Update details of a specific service       | Admin     |
| **Delete Service by ID**   | DELETE      | `/services/{id}`        | Delete a specific service                  | Admin     |
| **List Bookings**          | GET         | `/bookings/`            | Get all bookings                           | User      |
| **Create Booking**         | POST        | `/bookings/`            | Create a new booking                       | User      |
| **Retrieve Booking by ID** | GET         | `/bookings/{id}`        | Get details of a specific booking          | User      |
| **Update Booking by ID**   | PUT         | `/bookings/{id}`        | Update details of a specific booking       | User      |
| **Delete Booking by ID**   | DELETE      | `/bookings/{id}`        | Cancel a specific booking                  | User      |
| **List Reviews (Service)** | GET         | `/reviews/service/{id}` | Get all reviews for a specific service     | User      |
| **Create Review**          | POST        | `/reviews/`             | Add a review for a service                 | User      |
| **Update Review**          | PATCH       | `/reviews/{id}`         | Update a review                            | User      |
| **Delete Review**          | DELETE      | `/reviews/{id}`         | Delete a review                            | User      |
| **Swagger UI**             | -           | `/docs`                 | Interactive API documentation              | User      |
| **Swagger JSON**           | -           | `/openapi.json`         | OpenAPI JSON specification                 | User      |
| **ReDoc UI**               | -           | `/redoc`                | ReDoc API documentation                    | User      |
| **Health Check**           | GET         | `/`                     | Check API status                           | Public    |




##Env Variables
| Variable                      | Description                                 | Example Value                                         |
| ----------------------------- | ------------------------------------------- | ----------------------------------------------------- |
| `DATABASE_URL`                | PostgreSQL connection string                | `postgresql://user:password@localhost:5432/bookit_db` |
| `JWT_SECRET_KEY`              | Secret key for JWT token signing            | `supersecretkey`                                      |
| `JWT_ALGORITHM`               | Algorithm used for signing JWTs             | `HS256`                                               |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiration time for access tokens (minutes) | `15`                                                  |
| `REFRESH_TOKEN_EXPIRE_DAYS`   | Expiration time for refresh tokens (days)   | `7`                                                   |
?


## How to Run Locally

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/bookit-backend.git
   cd bookit-backend


2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3. Install dependencies
pip install -r requirements.txt

4. Set environment variables
DATABASE_URL=postgresql://postgres:1234@localhost:5432/bookit_db
JWT_SECRET=supersecretkey
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

5. Run database migrations
alembic upgrade head


7. Start the application
uvicorn main:app --reload
