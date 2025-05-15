# CarRentalDjango

A comprehensive car rental management system built with Django, designed to streamline the process of renting vehicles online.

## 📋 Overview

CarRentalDjango is a web-based application that facilitates the management of car rental services. The system provides an intuitive interface for both customers and administrators, enabling efficient vehicle rental processing, booking management, and administrative operations.

## ✨ Features

### Customer Panel
- **User Registration and Authentication**: Secure sign-up and login system for customers
- **Vehicle Search**: Filter vehicles by location, type, availability, and other criteria
- **Booking Management**: View, create, and manage rental bookings
- **Profile Management**: Update personal information and view rental history

### Admin/Dealer Panel
- **Dashboard**: Overview of bookings, revenue, and available vehicles
- **Inventory Management**: Add, edit, and remove vehicles from the fleet
- **Booking Control**: Approve, decline, or modify booking requests
- **User Management**: Manage customer accounts and permissions

## 🔧 Technology Stack

- **Backend**: Django (Python web framework)
- **Database**: SQLite (default) / PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Django Authentication System
- **Forms**: Django Forms with validation
- **ORM**: Django ORM for database interactions

## 🏗️ Project Structure

```
CarRentalDjango/
│
├── carrentalsystem/            # Main Django project folder
│   ├── settings.py             # Project settings
│   ├── urls.py                 # Main URL routing
│   └── wsgi.py                 # WSGI configuration
│
├── vehicles/                   # Vehicle app
│   ├── models.py               # Vehicle and related models
│   ├── views.py                # Vehicle-related views
│   ├── urls.py                 # URL patterns for vehicle app
│   └── templates/              # Templates for vehicle views
│
├── bookings/                   # Booking app
│   ├── models.py               # Booking and related models
│   ├── views.py                # Booking-related views
│   ├── urls.py                 # URL patterns for booking app
│   └── templates/              # Templates for booking views
│
├── accounts/                   # User accounts app
│   ├── models.py               # User profile models
│   ├── views.py                # Authentication and user-related views
│   ├── urls.py                 # URL patterns for accounts app
│   └── templates/              # Templates for account views
│
├── static/                     # Static files (CSS, JS, images)
│   ├── css/                    # Stylesheets
│   ├── js/                     # JavaScript files
│   └── images/                 # Image assets
│
├── media/                      # User-uploaded content
│
├── templates/                  # Global templates
│   ├── base.html               # Base template for inheritance
│   ├── home.html               # Homepage template
│   └── ...                     # Other global templates
│
├── manage.py                   # Django management script
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## 🛠️ Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JakubPoltorak147/CarRentalDjango.git
   cd CarRentalDjango
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin)**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - Website: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## 🔐 Environment Variables

For production deployment, configure the following environment variables:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string
- `STATIC_ROOT`: Path for collected static files
- `MEDIA_ROOT`: Path for media files

## 👥 User Roles

The system supports different user roles with specific permissions:

1. **Customer**
   - Browse and search vehicles
   - Make and manage bookings
   - View rental history
   - Submit reviews

2. **Admin/Dealer**
   - Manage vehicle inventory
   - Process bookings
   - Access reports and analytics
   - Manage user accounts

3. **Superadmin**
   - Full system access
   - Configure system settings
   - Manage all users and their permissions

## 📋 Future Enhancements

- Mobile application integration
- Payment gateway integration
- Advanced reporting and analytics
- Geolocation-based vehicle tracking
- Loyalty program for returning customers
- Multi-language support

## 👨‍💻 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

- **Developer**: Jakub Półtorak
- **GitHub**: [JakubPoltorak147](https://github.com/JakubPoltorak147)

---

Made with ❤️ using Django and Python
