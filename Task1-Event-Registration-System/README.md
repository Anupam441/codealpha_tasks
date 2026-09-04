# Event Registration System - Backend

A RESTful backend API for an Event Registration System, built as part of the CodeAlpha Backend Development Internship. Users can register/login (JWT-secured), create and manage events, and register/cancel registrations for events, with duplicate-registration prevention and capacity checks.

## Features

- User registration and login with JWT authentication
- Passwords hashed with bcryptjs (never stored in plain text)
- Full CRUD for Events (Create, Read, Update, Delete)
- Event registration system with duplicate prevention and capacity checks
- Available seats calculation
- My Registered Events endpoint with populated event details
- Owner/admin-only restrictions on updating and deleting events
- Centralized error handling with consistent JSON responses
- Clean layered (MVC-style) architecture

## Tech Stack

- Node.js - JavaScript runtime
- Express.js - Web framework for the REST API
- MongoDB Atlas - Cloud NoSQL database
- Mongoose - ODM to model data and talk to MongoDB
- JWT (jsonwebtoken) - Stateless authentication tokens
- bcryptjs - Password hashing
- dotenv - Manage environment variables
- cors - Allow cross-origin requests
- nodemon - Auto-restart server during development

## Architecture

Client / Postman -> Express Server -> Routes -> Middleware -> Controllers -> Models -> MongoDB -> Response (JSON)

Routes decide which controller handles the request. Middleware verifies JWT tokens and handles errors. Controllers contain business logic. Models define schema and talk to MongoDB via Mongoose.

## Project Structure

- config/db.js
- controllers/authController.js, eventController.js, registrationController.js
- middleware/authMiddleware.js, errorMiddleware.js
- models/User.js, Event.js, Registration.js
- routes/authRoutes.js, eventRoutes.js, registrationRoutes.js
- .env, .gitignore, package.json, server.js, README.md

## Installation

npm install
npm run dev

## Environment Variables (.env)

PORT=5000
MONGO_URI=your MongoDB Atlas connection string
JWT_SECRET=event_registration_secret_2026
JWT_EXPIRE=7d

Uses MongoDB Atlas (cloud) - no local MongoDB installation required.

## Authentication

All protected routes require a JWT sent in the header: Authorization: Bearer your_jwt_token
Get this token from the /api/auth/register or /api/auth/login response.

## Database Structure

User: name, email (unique), password (hashed), role (user/admin), timestamps
Event: title, description, date, location, capacity, createdBy (ref User), timestamps
Registration: user (ref User), event (ref Event), registeredAt - with a compound unique index on (user, event) to prevent duplicate registrations

## API Documentation

### Auth Routes (Public)
POST /api/auth/register - Public
POST /api/auth/login - Public

### Event Routes
GET /api/events - Public
GET /api/events/:id - Public
POST /api/events - Private (logged-in)
PUT /api/events/:id - Private (owner/admin only)
DELETE /api/events/:id - Private (owner/admin only)

### Registration Routes (all Private)
POST /api/registrations/:eventId
DELETE /api/registrations/:eventId
GET /api/registrations/my-events

## Testing Order

1. Start server (npm run dev)
2. Register a user
3. Login and copy JWT token
4. Create an event (with token)
5. Get all events
6. Get single event
7. Register for the event
8. View my registered events
9. Cancel registration
10. Update the event
11. Delete the event

All 11 steps were verified working end-to-end using an automated PowerShell test script hitting the live API.

## Future Improvements

- Pagination and search/filter for events
- Email notifications on registration
- Role-based admin dashboard
- Rate limiting and request validation
- Unit and integration tests

## Author

Anupam Yadav
CodeAlpha Backend Development Internship Submission
