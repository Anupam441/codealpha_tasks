# Important Backend Concepts (Hinglish)

## Node.js
JavaScript ko backend (server) par chalane deta hai. Non-blocking, asynchronous runtime.

## Express.js
Node.js ke upar ek lightweight framework jo routing aur middleware handling ko simple banata hai.

## REST API
Rules ka set jisse client-server URL aur HTTP methods se baat karte hain. Resources URLs se represent hote hain.

## HTTP Methods
GET - data fetch karna. POST - naya data create karna. PUT - existing data update karna. DELETE - data delete karna.

## Request and Response
Client server ko Request bhejta hai, server Response wapas bhejta hai (usually JSON).

## req.body
Client ne jo JSON data bheja hai (POST/PUT requests mein), yahan milta hai.

## req.params
URL ke andar ka dynamic part, jaise /events/:id mein id ki value.

## req.headers
Extra info jaise Authorization token, Content-Type.

## Middleware
Route aur Controller ke beech chalne wala function. Request ko modify ya block kar sakta hai. Security guard jaisa kaam karta hai.

## next()
Middleware ko bolta hai ki uska kaam ho gaya, ab agle function ko chalao.

## Controller
Business logic yahan hoti hai - manager jaisa, decide karta hai kya karna hai.

## Model
Database ka blueprint. Schema define karta hai data kaisa dikhega.

## Schema
Mongoose ka tareeka jisse hum data ke fields, types, aur rules define karte hain.

## MongoDB
NoSQL database jo JSON jaisa flexible data store karta hai.

## Mongoose
MongoDB ke liye ODM library, schema aur queries likhna easy banata hai.

## populate()
Jab kisi field mein sirf ObjectId store hota hai (reference), populate se uska poora data nikal lete hain.

## ObjectId
MongoDB ka unique 12-byte identifier har document ke liye.

## JWT (JSON Web Token)
Ek secure token jisme user info hoti hai. Server ko session store nahi karna padta (stateless auth).

## bcrypt
Password ko hash karne wali library. One-way hashing, reverse nahi ho sakta.

## Authentication
Tum kaun ho, yeh verify karna (login).

## Authorization
Tumhe yeh karne ki permission hai ya nahi, yeh check karna (jaise sirf owner event delete kar sake).

## HTTP Status Codes
200 OK - success. 201 Created - naya resource bana. 400 Bad Request - galat input. 401 Unauthorized - login nahi hai. 403 Forbidden - permission nahi hai. 404 Not Found - resource nahi mila. 500 Server Error - server ki taraf se galti.

## CRUD
Create, Read, Update, Delete - data ke saath basic operations.

## MVC / Layered Architecture
Code ko Model, View/Controller, aur Routes mein alag rakhna. Isse code organized aur maintainable rehta hai.

## Environment Variables
.env file mein secrets (jaise database URL, JWT secret) rakhte hain, taaki wo code mein hardcode na ho aur GitHub par public na ho.
