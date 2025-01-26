# 🎓 College Appointments API Documentation

## 🌐 System Overview

Welcome to the College Appointments API, an innovative web application designed to streamline interactions between students and professors. This comprehensive system leverages cutting-edge technologies to provide a seamless authentication and appointment scheduling experience.

### 🔧 Technical Architecture
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Token)
- **Primary Goal**: Facilitate efficient academic interactions

## 💾 Database Management

### Configuration Details
- **Database Name**: `college_appointments`

#### Essential Database Commands
```bash
# List all databases
show dbs

# Switch to college appointments database
use college_appointments

# Display available collections
show collections
```

## 🔐 Authentication Workflow

### 👥 Student Journey

#### 1. Student Registration
**Endpoint**: `localhost:8000/api/v1/signup_student`
- **HTTP Method**: POST
- **Registration Process**:
  ```json
  {
    "name": "Student Name",
    "email": "student@example.com",
    "password": "secure_password"
  }
  ```
- **Automatic Generation**:
  ✅ Unique MongoDB ID
  ✅ Secure password hashing
  ✅ Automatic enrollment number
  ✅ Account creation timestamp

#### 2. Student Login
**Endpoint**: `localhost:8000/api/v1/login_student`
- **HTTP Method**: POST
- **Login Credentials**:
  ```json
  {
    "enrollment_no": 1,
    "password": "secure_password"
  }
  ```
- **Authentication Highlights**:
  🔑 Profile information retrieval
  🎫 JWT token generation
  ✅ Secure access mechanism

### 👨‍🏫 Professor Authentication

#### 1. Professor Registration
**Endpoint**: `localhost:8000/api/v1/signup_prof`
- **HTTP Method**: POST
- **Registration Details**:
  ```json
  {
    "name": "Professor Name",
    "email": "professor@example.com",
    "password": "academic_password"
  }
  ```
- **Registration Features**:
  ✅ Professor profile creation
  🕒 Pre-configured time slots (8 AM - 5 PM)
  🟢 Flexible availability management

#### 2. Professor Login
**Endpoint**: `localhost:8000/api/v1/login_prof`
- **HTTP Method**: POST
- **Login Process**:
  ```json
  {
    "email": "professor@example.com",
    "password": "academic_password"
  }
  ```
- **Login Capabilities**:
  🔐 Secure authentication
  📋 Comprehensive profile access
  🎫 JWT token generation

## 🛡️ Security Architecture

### Advanced Security Features
- **Password Protection**:
  - BCrypt hashing algorithm
  - Cryptographic password storage
- **Authentication Mechanism**:
  - Role-based access control
  - Stateless JWT token authentication
- **Data Integrity**:
  - Secure transmission
  - Encrypted credentials

## 📊 Data Models

### 🧑 Student Document Structure
```json
{
  "_id": "Unique MongoDB Identifier",
  "name": "Student's Full Name",
  "email": "student@email.com",
  "enrollment_no": "Unique Enrollment ID",
  "created_at": "Account Creation Timestamp",
  "enrolled_courses": "Future Course Enrollment"
}
```

### 👩‍🏫 Professor Document Structure
```json
{
  "_id": "Unique MongoDB Identifier",
  "name": "Professor's Full Name",
  "email": "professor@email.com",
  "time_slots": {
    "8-17": "Hourly Availability Status"
  }
}
```

## 🚀 Future Enhancement Roadmap

### Planned Improvements
1. 📧 Enhanced email validation mechanisms
2. 🔐 Advanced password complexity requirements
3. 📅 Comprehensive time slot management
4. 🔄 Robust token refresh strategy

## 💡 Key Architectural Insights
- **Scalable Design**: Flexible and extensible system architecture
- **Secure Authentication**: Multi-layered security approach
- **Intelligent Metadata Management**: Automated profile enrichment
- **Standardized API Response**: Consistent and predictable interactions

---

**Note**: This documentation represents a professional-grade overview of the College Appointments API, emphasizing its technological sophistication and user-centric design.
