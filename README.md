# Task Management App

This is a Django-based task management system designed to track tasks, worked hours, and completion reports. The application features a role-based permission system with three user types: Users, Admins, and SuperAdmins.

## Features

***User:** View tasks, mark them as complete, and submit reports with their worked hours.

*** Admin:** Allows assigning new tasks and reviewing the completion reports.

***SuperAdmin** Allows create, edit, and delete any user; view every task in the system,promote regular users to the Admin role or demote them.

## Tech Stack

* **Python** & **Django**
* **Django REST Framework** 
* **Django REST Framework Simple JWT** 
* **SQLite3**

---
## Setup and Installation


1.  **Clone the Repo**
    ```bash
    git clone 
    cd 
    ```

2.  **Set Up Your Virtual Environment**
    ```bash
    # Create the environment
    python -m venv venv

    # On Windows
    venv\Scripts\activate

    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database**
    initial migrations
    ```bash
    python manage.py migrate
    ```

5.  **Create Django Superuser Account**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Running server**
    ```bash
    python manage.py runserver
    ```
    app will run at `http://127.0.0.1:8000/`.

6.  **Final Steps**
    After Superuser creation, use the superuser credentials to login to the Dashboard.
    Create a user
    Promote the user to admin
    Create another user
    Use the `edit` feature to assign the user to an admin

    


---
## API Endpoints


`POST` : `/api/token/`               | Log in for access/refresh tokens.
`POST` : `/api/token/refresh/`       | Get New access token
`GET`  : `/api/tasks/`               | View all Tasks 
`PUT`  : `/api/tasks/{id}/complete/` | Mark task as done.
`GET`  : `/api/tasks/{id}/report/`   | View Reports

---

### User Workflow
The user authenticates via the `/api/token/` endpoint to receive a JWT. Using this token, they fetch their assigned tasks from `/api/tasks/` and submit completed work via a `PUT` request to `/api/tasks/{id}/complete/`, including a report and worked hours.

### Admin Workflow
The Admin logs into the web dashboard. Their view is filtered to show only tasks assigned to users they manage. They can create new tasks for these users and review submitted completion reports. Their access is strictly limited to task management within their scope.

### SuperAdmin Workflow
The SuperAdmin has full system privileges via the web dashboard. They are responsible for all user account management (CRUD), role assignment (promoting/demoting Admins), and assigning users to be managed by Admins. They have a global view of all tasks and reports.