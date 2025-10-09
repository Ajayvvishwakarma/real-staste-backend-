# MongoDB Setup Complete ✅

## Configuration

### MongoDB Connection
- **URL**: mongodb+srv://amit24ve:Amit%402403.@trading.70xxozj.mongodb.net/
- **Database**: 99acres_db
- **Connection**: Motor (async MongoDB driver)

## What Was Done

### 1. Updated Config (`app/config.py`)
- Set MONGODB_URL to your connection string
- Added DATABASE_NAME for the database

### 2. Created MongoDB Database Module (`app/database/mongodb.py`)
- Connection management (connect_to_mongo, close_mongo_connection)
- Index creation for better performance
- Sample data creation (users and properties)

### 3. Created MongoDB Models (`app/database/mongo_models.py`)
- Pydantic v2 compatible models
- User, Property, Appointment, Contact models
- Custom PyObjectId handler for MongoDB ObjectIds

### 4. Created MongoDB User Repository (`app/database/repositories/mongo_user_repository.py`)
- create_user
- get_user_by_id
- get_user_by_email
- get_user_from_token
- update_user
- update_last_login
- delete_user
- get_users (with filters)
- count_users

### 5. Created MongoDB Auth Routes (`app/routes/auth_mongo.py`)
- POST /register - Register new user
- POST /login - Login with email and password
- GET /profile - Get current user profile (protected)
- POST /logout - Logout

### 6. Updated Main App (`main.py`)
- Uses MongoDB instead of SQLite
- Connects to MongoDB on startup
- Creates sample data if database is empty
- Closes connection on shutdown

## Sample Users Created

1. **Admin**
   - Email: admin@99acres.com
   - Password: admin123
   - Role: admin

2. **Your Account**
   - Email: ajayvishwakrma1@gmail.com
   - Password: Ajay@123
   - Role: client

3. **Agent**
   - Email: agent@99acres.com
   - Password: agent123
   - Role: agent

## API Endpoints

### Authentication
- POST `/api/auth/register` - Register new user
- POST `/api/auth/login` - Login
- GET `/api/auth/profile` - Get profile (requires token)
- GET `/api/profile` - Get profile (requires token)
- POST `/api/auth/logout` - Logout

### How to Use

1. **Register**:
```json
POST http://localhost:8000/api/auth/register
{
    "email": "user@example.com",
    "name": "User Name",
    "password": "password123",
    "phone": "1234567890",
    "user_type": "client"
}
```

2. **Login**:
```json
POST http://localhost:8000/api/auth/login
{
    "email": "ajayvishwakrma1@gmail.com",
    "password": "Ajay@123",
    "user_type": "client"
}
```

3. **Get Profile**:
```
GET http://localhost:8000/api/profile
Headers: Authorization: Bearer YOUR_TOKEN_HERE
```

## MongoDB Collections

1. **users** - User accounts with authentication
2. **properties** - Real estate properties
3. **appointments** - Property viewing appointments
4. **contacts** - Contact form submissions

## Indexes Created

### Users Collection
- email (unique)
- phone
- role

### Properties Collection
- owner_id
- city
- property_type
- status
- price

### Appointments Collection
- user_id
- property_id
- appointment_date

## Features

✅ Full MongoDB integration
✅ Async operations with Motor
✅ JWT token authentication
✅ Password hashing with bcrypt
✅ Pydantic v2 validation
✅ Sample data auto-creation
✅ Index optimization
✅ CORS enabled for frontend
✅ Protected routes with Bearer token
✅ User role management (admin, agent, client, subuser)

## Frontend Integration

Update your frontend API base URL to:
```javascript
const API_URL = "http://localhost:8000/api";
```

Store the token after login:
```javascript
localStorage.setItem('token', response.token);
```

Include token in requests:
```javascript
headers: {
  'Authorization': `Bearer ${localStorage.getItem('token')}`,
  'Content-Type': 'application/json'
}
```

## Server Status

The server should now be running with MongoDB!

Check the console for:
- ✅ Successfully connected to MongoDB!
- 📊 Database: 99acres_db
- 📑 Database indexes created successfully!
- ✅ Created 3 sample users
- ✅ Created 2 sample properties

## Testing

You can test the endpoints using:
1. Postman
2. cURL
3. Your React frontend (update API URL to port 8000)

## Notes

- SQLite code is still in the project but not being used
- All data is now stored in MongoDB Atlas
- Token expires in 30 minutes (configurable in config.py)
- CORS is configured for localhost:3004 and localhost:3000