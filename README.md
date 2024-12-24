# EaseWork

## - Household Services Application - V2

A multi-user web application providing a platform for comprehensive home servicing and solutions. This project demonstrates role-based access control (RBAC) with three user roles: **Admin**, **Service Professionals**, and **Customers**, offering a seamless interface to manage service requests and professional assignments. This application is built using Flask, SQLite, and VueJS with additional support for Redis and Celery for asynchronous tasks and caching. It includes features like admin control over users, service requests by customers, professional management, and scheduled batch jobs.

---

## Features by Role

### Admin
- Root access without the need for registration.
- **Admin Dashboard**: View and manage all users and service professionals.
- **Service Management**: Create, update, and delete services.
- **Approval**: Verify and approve service professionals based on document uploads.
- **Block/Unblock Users**: Manage access for customers or professionals based on activity/reviews.
- **Service Professional Search**: Find professionals for review and management.

### Service Professional
- **Registration/Login**: Register with required professional details and uploaded documents for approval.
- **Service Requests**: View, accept, or reject customer service requests.
- **Close Requests**: Mark service requests as completed after customer confirmation.
- **Export Service Requests**: Export closed service requests to a CSV file for record-keeping.
- **Notifications**: Receive reminders about pending or unvisited service requests.

### Customer
- **Registration/Login**: Create an account to book services.
- **Service Requests**: Search for available services by name, pin code, or location.
- **Request Management**: Open, edit, and close service requests.
- **Post Reviews**: Submit reviews for completed services to help others find top-rated professionals.
- **Monthly Reports**: Receive detailed reports of services requested and completed via email.

---

## Technologies Used
- **Backend**: Flask (Python) with Flask-RESTful and Flask-SQLAlchemy for APIs and database management.
- **Frontend**: VueJS with CLI for advanced UI development.
- **Database**: SQLite for storing application data.
- **Styling**: Bootstrap for responsive and styled HTML components.
- **Caching & Batch Jobs**:
  - Redis for performance improvement and caching.
  - Celery for managing asynchronous batch jobs and scheduled tasks.
- **Task Scheduling**:
  - Email for reminders.
  - Monthly activity reports sent via email.

---

## Installation and Setup

### Prerequisites
- Python 3.x
- Node.js and npm
- Redis server

### Steps to Set Up the Project

#### 1. Clone the Repository:
```bash
git clone https://github.com/bhavyasharma2/EaseWork-Household-Services-App-V2.git
cd EaseWork-Household-Services-App-V2
```

#### 2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

#### 3. Initialize the SQLite database:
```bash
flask db init
flask db migrate
flask db upgrade
```

### 4. Start the Flask development server:
```bash
python app.py
```

### 5. Start the Redis server:
```bash
redis-server
```

### 6. Run the Celery worker and Celery Beat scheduler:
```bash
celery -A app.celery worker --loglevel=debug
celery -A Code.app.celery beat --schedule Code/celerybeat-schedule --loglevel=info
```
