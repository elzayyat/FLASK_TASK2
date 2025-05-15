# Flask ToDo Application
A feature-rich ToDo application built with Flask, MySQL, and Bootstrap. This application allows users to register, login, create tasks, mark them as complete/incomplete, and delete tasks. It also includes an admin panel for user management.

## Features
- User registration and authentication
- Email-based login system
- User-specific task management
- Create, read, update, and delete tasks
- Mark tasks as complete/incomplete
- Admin dashboard for user management
- Responsive UI with Bootstrap
- Dockerized application for easy deployment
## Project Structure
## Technologies Used
- Backend : Flask 2.0.1
- Database : MySQL 8.0
- ORM : SQLAlchemy 2.5.1
- Authentication : Flask-Login 0.5.0
- Forms : Flask-WTF 0.15.1
- Frontend : Bootstrap (via Flask-Bootstrap 3.3.7.1)
- Containerization : Docker
## Setup Instructions
### Local Development
1. Clone the repository:
2. Install dependencies:
3. Set up MySQL database:
4. Update database connection in app.py if needed:
5. Run the application:
6. Access the application at http://localhost:5000
### Docker Deployment
1. Make sure Docker and Docker Compose are installed on your system
2. Build and run the containers:
3. Access the application at http://localhost:5000
## Docker Configuration
The application is containerized using Docker with the following configuration:

- Web Service : Flask application running on port 5000
- Database Service : MySQL 8.0 with data persistence
- Port Mapping :
  - Flask app: 5000:5000
  - MySQL: 3307:3306 (to avoid conflicts with local MySQL)
## User Roles
### Regular User
- Register an account
- Login with email and password
- Create, view, update, and delete personal tasks
- Mark tasks as complete/incomplete
### Admin User
- Access to admin dashboard
- View all users and their tasks
- Manage user accounts
## Default Admin Account
An admin account is automatically created when the application starts:

- Email: admin@example.com
- Password: adminpassword
## License
MIT License
