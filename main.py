from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import auth, users, services, bookings, review

app = FastAPI(
    title="BookIt API",
    description="A booking management API",
    version="1.0.0",
    openapi_tags=[
        {"name": "auth", "description": "Authentication (register, login, refresh, logout)"},
        {"name": "users", "description": "User profile management"},
        {"name": "services", "description": "Service management"},
        {"name": "bookings", "description": "Booking management"},
        {"name": "reviews", "description": "Reviews and ratings"},
        {"name": "health", "description": "API health check"},
    ],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(services.router, prefix="/services", tags=["services"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
app.include_router(review.router, prefix="/reviews", tags=["reviews"])

# Health check
@app.get("/", tags=["health"])
def root():
    return {
        "message": "BookIt API is running",
        "status": "healthy",
        "version": "1.0.0",
    }
