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
├── car_dealer_portal/          # Dealer portal application
│   ├── __pycache__/            # Python cache files
│   ├── migrations/             # Database migrations
│   ├── templates/              # View templates
│   │   └── car_dealer/         # Dealer-specific templates
│   │       ├── activation_failed.html
│   │       ├── activation_success.html
│   │       ├── base.html
│   │       ├── confirm_complete_order.html
│   │       ├── confirm_delete_vehicle.html
│   │       ├── history.html
│   │       ├── home_page.html
│   │       ├── login.html
│   │       ├── login_failed.html
│   │       ├── manage.html
│   │       ├── order_detail.html
│   │       ├── order_list.html
│   │       ├── password_reset_success.html
│   │       ├── profile_updated.html
│   │       ├── register.html
│   │       ├── registered.html
│   │       ├── registration_error.html
│   │       ├── registration_pending.html
│   │       ├── reset_password_confirm.html
│   │       ├── reset_password_email_sent.html
│   │       ├── reset_password_request.html
│   │       ├── update_profile.html
│   │       ├── vehicle_added.html
│   │       └── vehicle_detail.html
│   ├── __init__.py
│   ├── admin.py                # Admin panel configuration
│   ├── apps.py                 # Application configuration
│   ├── models.py               # Data models
│   ├── tests.py                # Tests
│   ├── urls.py                 # URL routing for dealer portal
│   └── views.py                # Dealer portal views
│
├── customer_portal/            # Customer portal application
│   ├── __pycache__/            # Python cache files
│   ├── migrations/             # Database migrations
│   ├── templates/              # View templates
│   │   └── customer/           # Customer-specific templates
│   │       ├── account_activated.html
│   │       ├── activation_failed.html
│   │       ├── all_cars.html
│   │       ├── base.html
│   │       ├── confirmation.html
│   │       ├── confirmed.html
│   │       ├── home_page.html
│   │       ├── login.html
│   │       ├── login_failed.html
│   │       ├── manage.html
│   │       ├── order_detail.html
│   │       ├── order_failed.html
│   │       ├── password_reset_success.html
│   │       ├── profile_updated.html
│   │       ├── register.html
│   │       ├── registration_error.html
│   │       ├── registration_pending.html
│   │       ├── reset_password_confirm.html
│   │       ├── reset_password_email_sent.html
│   │       ├── reset_password_request.html
│   │       ├── search.html
│   │       ├── search_results.html
│   │       ├── update_profile.html
│   │       └── vehicle_details.html
│   ├── __init__.py
│   ├── admin.py                # Admin panel configuration
│   ├── apps.py                 # Application configuration
│   ├── models.py               # Data models
│   ├── tests.py                # Tests
│   ├── urls.py                 # URL routing for customer portal
│   └── views.py                # Customer portal views
│
├── home/                       # Home page application
│   ├── __pycache__/            # Python cache files
│   ├── migrations/             # Database migrations
│   ├── templates/              # View templates
│   │   └── home/               # Home page templates
│   │       └── index.html      # Home page
│   ├── __init__.py
│   ├── admin.py                # Admin panel configuration
│   ├── apps.py                 # Application configuration
│   ├── models.py               # Data models
│   ├── tests.py                # Tests
│   ├── urls.py                 # URL routing for home page
│   └── views.py                # Home page views
│
├── media/                      # User-uploaded content
│   └── vehicles/               # Vehicle images (e.g., audi-a4.jpg, bmw-x1.jpg)
│
├── vehicles/                   # Vehicles application (empty structure, functionality in other apps)
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
   - Manage account settings

2. **Admin/Dealer**
   - Manage vehicle inventory
   - Process bookings
   - Manage account settings

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
