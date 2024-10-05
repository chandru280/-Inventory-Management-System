# Inventory Management System

This project is an **Inventory Management System** built with **Django** and **Django REST Framework (DRF)**. The system provides APIs to manage inventory items, register users, handle user authentication with JWT tokens, and enable user logout. The backend uses **PostgreSQL** as the database, and **Redis** for caching to improve performance.

## Features

- **Inventory Management**: Create, read, update, and delete inventory items.
- **User Authentication**: JWT-based authentication to secure access to the system.
- **User Registration**: New users can register and create an account.
- **Logout**: Authenticated users can log out.
- **Caching**: Redis is used for caching frequently accessed data.

## Requirements

To run the project, you need the following Python packages:

- **asgiref**: Version 3.8.1
- **Django**: Version 5.1.1
- **django-environ**: Version 0.11.2
- **django-redis**: Version 5.4.0
- **djangorestframework**: Version 3.15.2
- **djangorestframework-simplejwt**: Version 5.3.1
- **psycopg2-binary**: Version 2.9.9
- **PyJWT**: Version 2.9.0
- **redis**: Version 5.0.8
- **sqlparse**: Version 0.5.1

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd inventory-management-system
