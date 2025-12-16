#  STEMAIDE LMS Backend API

This is the **Django REST API backend** for the **STEMAIDE Learning Management System (LMS)**.  
It provides secure and scalable endpoints for managing users, courses, enrollment, and authentication.  
Authentication is powered by **Knox** for secure access and session management.

---

##  Features

- User registration and login via **JWT authentication**
- User roles (Admin, Instructor, Student)
- Course management (create, update, delete, and view courses)
- Enrollment and progress tracking
- Secure RESTful API using **Django REST Framework (DRF)**
- Auto timestamps for creation and modification
- Modular and scalable architecture for future extensions

---

##Tech Stack

- **Backend Framework:** Django, Django REST Framework  
- **Authentication:**knox  
- **Database:** SQLite (development) / PostgreSQL (production)  
- **Language:** Python 3.10+  
- **Version Control:** Git & GitHub  

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/sammyyaws/LMS.git
cd LMS
