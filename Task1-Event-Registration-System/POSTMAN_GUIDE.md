# Postman Testing Guide

Base URL: http://localhost:5000

How to use your JWT token: After Register or Login, copy the token value from the response. For every protected route, in Postman go to Authorization tab, select Bearer Token, and paste the token.

## 1. Register User
Method: POST
URL: http://localhost:5000/api/auth/register
Body (raw JSON):
{ "name": "Ayush", "email": "ayush@gmail.com", "password": "123456" }
Expected: 201 Created with user data and token

## 2. Login User
Method: POST
URL: http://localhost:5000/api/auth/login
Body: { "email": "ayush@gmail.com", "password": "123456" }
Expected: 200 OK with user data and token

## 3. Create Event
Method: POST
URL: http://localhost:5000/api/events
Auth: Bearer Token required
Body: { "title": "Tech Conference 2026", "description": "Technology and AI conference", "date": "2026-10-15T10:00:00.000Z", "location": "Kanpur", "capacity": 100 }
Expected: 201 Created with event data

## 4. Get All Events
Method: GET
URL: http://localhost:5000/api/events
Auth: None (public)
Expected: 200 OK with array of events

## 5. Get Single Event
Method: GET
URL: http://localhost:5000/api/events/eventId
Auth: None (public)
Expected: 200 OK with event data including registeredCount and availableSeats

## 6. Update Event
Method: PUT
URL: http://localhost:5000/api/events/eventId
Auth: Bearer Token required (owner or admin only)
Body example: { "location": "Delhi" }
Expected: 200 OK with updated event

## 7. Delete Event
Method: DELETE
URL: http://localhost:5000/api/events/eventId
Auth: Bearer Token required (owner or admin only)
Expected: 200 OK, event and its registrations deleted

## 8. Register for Event
Method: POST
URL: http://localhost:5000/api/registrations/eventId
Auth: Bearer Token required
Expected: 201 Created. If already registered, 400 error. If event full, 400 error.

## 9. Cancel Registration
Method: DELETE
URL: http://localhost:5000/api/registrations/eventId
Auth: Bearer Token required
Expected: 200 OK

## 10. My Registered Events
Method: GET
URL: http://localhost:5000/api/registrations/my-events
Auth: Bearer Token required
Expected: 200 OK with array of registrations including populated event details

