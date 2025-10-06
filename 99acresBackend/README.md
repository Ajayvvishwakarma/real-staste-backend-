# 99Acres Real Estate Backend API

A comprehensive FastAPI backend for the 99Acres real estate application with MongoDB database.

## Features

- 🚀 **FastAPI Framework** - Modern, fast web framework for building APIs
- 🍃 **MongoDB Database** - NoSQL database with Beanie ODM
- 🔐 **JWT Authentication** - Secure user authentication and authorization
- 👥 **Role-Based Access Control** - Multiple user roles (Super Admin, Admin, Staff, Agent, Client, Subuser)
- 🏠 **Property Management** - Complete CRUD operations for properties
- 📅 **Appointment System** - Schedule and manage property viewings
- 📞 **Contact & Inquiry Management** - Handle customer inquiries and callbacks
- 📊 **Dashboard Analytics** - User and admin dashboards with statistics
- 📁 **File Upload Support** - Property images and document uploads
- 🔍 **Advanced Search & Filtering** - Property search with multiple filters
- 📄 **Auto-generated API Documentation** - Interactive API docs with Swagger/OpenAPI

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **Database**: MongoDB with Beanie ODM
- **Authentication**: JWT with bcrypt password hashing
- **File Handling**: Built-in file upload support
- **Documentation**: Automatic OpenAPI/Swagger documentation
- **CORS**: Configured for frontend integration

## Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **MongoDB** installed and running locally or MongoDB Atlas account
3. **Git** (optional, for cloning)

### Installation

#### Option 1: Automated Setup (Recommended)

**For Windows:**
```bash
# Run the setup script
setup.bat
```

**For Linux/Mac:**
```bash
# Make script executable and run
chmod +x setup.sh
./setup.sh
```

#### Option 2: Manual Setup

1. **Create Virtual Environment**
```bash
python -m venv venv
```

2. **Activate Virtual Environment**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### Configuration

1. **Environment Variables**: Update `.env` file with your settings:
```env
MONGODB_URL=mongodb://localhost:27017/99acres_db
SECRET_KEY=your-super-secret-key-here
```

2. **MongoDB Setup**: Ensure MongoDB is running on your system

### Running the Application

```bash
# Make sure virtual environment is activated
python -m app
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/client-login` - Client-specific login
- `POST /api/auth/subuser-login` - Subuser login
- `POST /api/auth/logout` - User logout

### Users
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update user profile
- `GET /api/users` - List users (Admin)
- `POST /api/users` - Create user (Admin)
- `GET /api/users/stats` - User statistics

### Properties
- `GET /api/properties` - List properties with search/filter
- `POST /api/properties` - Create new property
- `GET /api/properties/{id}` - Get property details
- `PUT /api/properties/{id}` - Update property
- `DELETE /api/properties/{id}` - Delete property
- `GET /api/properties/my-properties` - User's properties
- `GET /api/properties/search` - Advanced property search

### Appointments
- `GET /api/appointments` - List appointments
- `POST /api/appointments` - Schedule appointment
- `GET /api/appointments/{id}` - Get appointment details
- `PUT /api/appointments/{id}` - Update appointment
- `DELETE /api/appointments/{id}` - Cancel appointment
- `GET /api/appointments/stats` - Appointment statistics

### Contacts & Inquiries
- `POST /api/contacts` - Submit contact form
- `POST /api/contacts/inquiries` - Submit property inquiry
- `POST /api/contacts/callback` - Request callback
- `GET /api/contacts` - List contacts (Admin)
- `GET /api/contacts/inquiries` - List inquiries (Admin)
- `GET /api/contacts/stats` - Contact statistics

### Dashboard
- `GET /api/dashboard/user` - User dashboard
- `GET /api/dashboard/admin` - Admin dashboard
- `GET /api/dashboard/stats` - General statistics
- `GET /api/dashboard/property-stats` - Property statistics
- `GET /api/dashboard/activity` - Recent activity

### Admin
- `GET /api/admin/dashboard` - Admin dashboard
- `GET /api/admin/users` - Manage users
- `GET /api/admin/properties` - Manage properties
- `PUT /api/admin/users/{id}/block` - Block/unblock user
- `PUT /api/admin/properties/{id}/approve` - Approve property

## Database Models

### User Model
- Multiple roles: Super Admin, Admin, Staff, Agent, Client, Subuser
- Profile information, contact details
- Authentication and authorization data

### Property Model
- Complete property information
- Images, documents, location data
- Status management (Active, Pending, Sold, etc.)
- Search and filter capabilities

### Appointment Model
- Property viewing appointments
- User and agent assignment
- Status tracking and management

### Contact & Inquiry Models
- Customer inquiries and contact forms
- Callback request management
- Status tracking and responses

## User Roles & Permissions

1. **Super Admin**: Full system access
2. **Admin**: Manage users, properties, and system operations
3. **Staff**: Limited administrative access
4. **Agent**: Property management and client interactions
5. **Client**: Property browsing and inquiries
6. **Subuser**: Limited client access

## File Upload Support

- Property images
- Property documents
- User profile pictures
- Configurable file size and type restrictions

## Frontend Integration

This backend is designed to work seamlessly with the 99Acres frontend application:

- **CORS configured** for frontend domains
- **RESTful API design** matching frontend expectations
- **Consistent response formats** for easy frontend integration
- **Comprehensive error handling** with detailed error messages

## Development

### Project Structure
```
99acresBackend/
├── app/
│   ├── __init__.py
│   ├── __main__.py          # Main application entry point
│   ├── config.py            # Configuration settings
│   ├── database/
│   │   ├── __init__.py
│   │   ├── __init__db.py    # Database initialization
│   │   ├── models.py        # Database models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── repositories/    # Data access layer
│   ├── routes/              # API route handlers
│   └── utils/               # Utility functions
├── uploads/                 # File upload directory
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README.md               # This file
```

### Adding New Features

1. **Models**: Add new Beanie models in `app/database/models.py`
2. **Schemas**: Create Pydantic schemas in `app/database/schemas/`
3. **Repositories**: Add data access logic in `app/database/repositories/`
4. **Routes**: Create API endpoints in `app/routes/`
5. **Register Routes**: Add new routes in `app/__main__.py`

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Production Deployment

### Environment Variables for Production

```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/99acres_db
SECRET_KEY=your-super-secure-random-secret-key
DEBUG=False
ALLOWED_ORIGINS=["https://yourdomain.com"]
```

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "-m", "app"]
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Check the [API Documentation](http://localhost:8000/docs)
- Open an issue on GitHub
- Contact the development team

## Changelog

### Version 1.0.0
- Initial release
- Complete API implementation
- User authentication and authorization
- Property management system
- Appointment scheduling
- Contact and inquiry management
- Dashboard analytics
- File upload support