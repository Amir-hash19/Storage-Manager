# Storage manager Google Driver Clone

A scalable and maintainable backend API built with **Django**, **Django REST Framework**, and **JWT Authentication**, following **Clean Architecture**, **Service Layer**, **Repository Pattern**, and an **Event-Driven Architecture**.

One of the core modules is a **Google Drive-inspired Storage Manager**, providing hierarchical folder management, file organization, uploads, downloads, moving, renaming, and deletion through a RESTful API.

The project is fully containerized with **Docker Compose** and designed for scalability, maintainability, and clean separation of concerns.

---

# Features

- Clean Architecture
- Service Layer
- Repository Pattern
- Event-Driven Architecture
- JWT Authentication
- RESTful API
- Folder/File Management (Google Drive-like)
- Docker & Docker Compose
- Celery Background Tasks
- Redis Message Broker
- PostgreSQL Database
- Audit Logging
- Pagination
- Filtering & Searching
- Permission-based APIs
- Asynchronous Event Processing
- Ready for Horizontal Scaling

---

# Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| Django | Web Framework |
| Django REST Framework | REST API |
| PostgreSQL | Database |
| Redis | Cache & Message Broker |
| Celery | Background Tasks |
| JWT | Authentication |
| Docker | Containerization |
| Docker Compose | Local Development |
| Clean Architecture | Application Structure |
| Repository Pattern | Data Access Layer |
| Service Layer | Business Logic |
| Event Driven | Loose Coupling |

---

# Project Structure

```
project/
│
├── apps/
│   ├── useraccount/
│   ├── storage/
│   ├── dashboard/
│   └── auditlog/
│
├── config/
│
├── docker/
│
├── requirements/
│
├── docker-compose.yml
├── Dockerfile
└── manage.py
```

---

# Application Modules

## useraccount

Responsible for:

- User Registration
- Login
- JWT Authentication
- Profile Management
- Permissions
- User Events

---

## storage

Responsible for:

- Folder Management
- File Management
- Nested Directories
- Upload
- Download
- Rename
- Move
- Delete
- Storage Events

The storage system behaves similarly to **Google Drive**, allowing unlimited nested folders and files.

---

## dashboard

Responsible for:

- Dashboard Statistics
- Storage Overview
- User Metrics
- Activity Summary

---

## auditlog

Responsible for:

- Recording System Events
- Tracking User Activities
- Logging File Operations
- Authentication Logs
- Event History

---

# Architecture

This project follows **Clean Architecture** principles.

```
                 HTTP Request
                       │
                       ▼
                DRF View / API
                       │
                       ▼
                 Service Layer
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
 Repository Layer              Domain Events
        │                             │
        ▼                             ▼
   Django ORM                  Event Handlers
        │                             │
        └──────────────┬──────────────┘
                       ▼
                  PostgreSQL
```

Each layer has a single responsibility.

---

# Clean Architecture Layers

## Presentation Layer

Contains:

- Views
- Serializers
- Permissions
- Authentication
- API Validation

Responsibilities:

- Receive HTTP Requests
- Validate Input
- Return HTTP Responses

---

## Service Layer

Contains the complete business logic.

Responsibilities:

- Execute use cases
- Validate business rules
- Coordinate repositories
- Publish domain events

Example:

```
Create Folder

Request
    ↓
Serializer
    ↓
FolderService.create_folder()
    ↓
FolderRepository.create()
    ↓
FolderCreatedEvent
```

---

## Repository Layer

Responsible for database communication.

Responsibilities:

- Query Database
- Create Records
- Update Records
- Delete Records

Services never communicate directly with Django ORM.

Instead:

```
Service
    ↓
Repository
    ↓
ORM
```

---

## Domain Events

The application is loosely coupled using events.

Example events:

```
UserRegisteredEvent

UserLoggedInEvent

FolderCreatedEvent

FolderDeletedEvent

FolderRenamedEvent

FileUploadedEvent

FileDeletedEvent

FileMovedEvent

PasswordChangedEvent
```

Each event can have multiple listeners.

Example:

```
FolderCreatedEvent

        │
        ├────────► Audit Logger
        │
        ├────────► Dashboard Update
        │
        └────────► Notification
```

No module depends directly on another module.

---

# Folder Structure (Example)

```
storage/

├── api/
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── services/
│   ├── folder_service.py
│   └── file_service.py
│
├── repositories/
│   ├── folder_repository.py
│   └── file_repository.py
│
├── events/
│   ├── publishers.py
│   ├── handlers.py
│   └── events.py
│
├── models.py
├── permissions.py
└── signals.py
```

Every application follows the same architecture.

---

# Request Flow

```
Client
   │
   ▼
APIView
   │
   ▼
Serializer Validation
   │
   ▼
Service Layer
   │
   ▼
Repository Layer
   │
   ▼
Database
   │
   ▼
Publish Event
   │
   ▼
Event Handlers
   │
   ▼
Response
```

---

# Event Flow

```
Business Action
       │
       ▼
Publish Event
       │
       ▼
Event Dispatcher
       │
 ┌─────┼───────────┐
 ▼     ▼           ▼

Audit  Dashboard  Notifications
```

---

# Authentication

Authentication is implemented using **JWT**.

Typical flow:

```
Register

↓

Login

↓

Access Token

↓

Refresh Token

↓

Authenticated APIs
```

---

# API Endpoints

## Authentication

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login |
| POST | `/api/auth/refresh/` | Refresh JWT Token |
| POST | `/api/auth/logout/` | Logout |
| GET | `/api/auth/profile/` | Current User |
| PATCH | `/api/auth/profile/` | Update Profile |
| POST | `/api/auth/change-password/` | Change Password |

---

## Storage

### Folder APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/storage/folders/` | List folders |
| POST | `/api/storage/folders/` | Create folder |
| GET | `/api/storage/folders/{id}/` | Folder details |
| PATCH | `/api/storage/folders/{id}/` | Rename folder |
| DELETE | `/api/storage/folders/{id}/` | Delete folder |
| POST | `/api/storage/folders/{id}/move/` | Move folder |

---

### File APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/storage/files/` | List files |
| POST | `/api/storage/files/upload/` | Upload file |
| GET | `/api/storage/files/{id}/` | File details |
| GET | `/api/storage/files/{id}/download/` | Download file |
| PATCH | `/api/storage/files/{id}/` | Rename file |
| DELETE | `/api/storage/files/{id}/` | Delete file |
| POST | `/api/storage/files/{id}/move/` | Move file |

---

## Dashboard

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/dashboard/overview/` | Dashboard Overview |
| GET | `/api/dashboard/storage/` | Storage Statistics |
| GET | `/api/dashboard/activity/` | Recent Activities |

---

## Audit Logs

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/audit/logs/` | List Audit Logs |
| GET | `/api/audit/logs/{id}/` | Audit Log Details |

---

# Running with Docker

The project is fully containerized.

## Start

```bash
docker compose up --build
```

---

## Stop

```bash
docker compose down
```

---

## Run Migrations

```bash
docker compose exec web python manage.py migrate
```

---

## Create Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

---

## Run Tests

```bash
docker compose exec web pytest
```

---

# Services

Docker Compose starts the following services:

- Django API
- PostgreSQL
- Redis
- Celery Worker
- Celery Beat (optional)

---

# Why This Architecture?

This architecture provides:

- Clear separation of concerns
- Testable business logic
- Loosely coupled modules
- Easy scalability
- High maintainability
- Easy feature extension
- Independent domain components
- Minimal ORM dependency inside business logic

---

# Future Improvements

- API Versioning
- OpenAPI / Swagger Documentation
- WebSocket Notifications
- File Sharing
- Role-Based Access Control (RBAC)
- Object-Level Permissions
- Soft Delete
- Multi-Tenant Support
- Distributed Event Bus (Kafka/RabbitMQ)
- S3 / MinIO Storage
- Prometheus & Grafana Monitoring

---

# License

This project is intended as a production-ready backend template demonstrating Clean Architecture, Service Layer, Repository Pattern, and Event-Driven design using Django and Django REST Framework.