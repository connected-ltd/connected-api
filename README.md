# 📡 Connected API

This is the backend service powering the Connected platform, built with Flask and organized into modular components. It supports features like file uploads, shortcode integration, SMS and WhatsApp messaging, user management, and USSD operations.

---

## 📁 Project Directory Structure

The project follows a modular structure to organize routes, models, and schemas by feature. Here's an overview of each directory and file:

### Root-Level Files

- **`README.md`**: Provides an overview of the project, including setup instructions, usage guidelines, and other relevant documentation.

- **`Dockerfile`**: Contains instructions to build a Docker image for the application, enabling containerized deployments.

- **`main.py`**: The main entry point of the application.

- **`manage.py`**: Command-line tool for running administrative tasks like migrations and tests.

- **`run`**: Shell script or executable used to start the app in production or development.

- **`supervisord.conf`**: Configuration file for Supervisor to manage and auto-restart the backend process.

- **`.fs`**: Specifies Python package dependencies using [Flox](https://flox.dev/) or a similar package manager, as an alternative to `requirements.txt`.

---

### `app/` – Core Application Logic

Each feature module is structured using a **controller–model–schema** pattern:

- `__init__.py` – Initializes the app as a Python module.
- `error_handlers.py` – Global error handling logic.
- `route_guard.py` – Middleware for JWT-based authentication and route protection.

#### Domain Modules:

Each of the following contains logic specific to the domain it serves:

- **`areas/`**: Geographic area definitions and management.
- **`files/`**: Handles file uploads and metadata.
- **`messages/`**: Broadcast and SMS/WhatsApp messaging logic.
- **`numbers/`**: Phone number registration and association.
- **`shortcode_files/`**: Manages files linked to shortcode functionality.
- **`shortcodes/`**: Registration and use of shortcode services.
- **`user/`**: User account creation, login, and profiles.
- **`ussd/`**: Logic for USSD interactions and menu flows.
- **`whatsapp_number/`**: WhatsApp number registration and configuration.

Each of these contains:

- `controller.py` – API route handlers.
- `model.py` – SQLAlchemy database models.
- `schema.py` – Marshmallow schemas for input validation and serialization.

#### `celery/`

- `__init__.py` – Initializes Celery with Flask context.
- `tasks.py` – Defines asynchronous tasks (e.g., background jobs, notifications).

---

### `config/` – Configuration Utilities

Centralized configurations for services and app initialization:

- `__init__.py` – Loads the app configuration.
- `celery.py` – Celery configuration (e.g., broker URL, task settings).
- `db.py` – SQLAlchemy database configuration.
- `jwt.py` – JWT token creation, validation, and expiry management.
- `mail.py` – SMTP and email notification configuration.

---

### `helpers/` – Utility Functions and API Integrations

Reusable modules for third-party integrations and shared functionality:

- `africastalking.py` – Sends SMS via Africa’s Talking.
- `area_list.py` – Contains static or fetched geographic area names.
- `langchain.py` – AI integration using Langchain (e.g., OpenAI API).
- `twilio.py` – Sends WhatsApp messages via Twilio.
- `upload.py` – File upload utilities (e.g., cloud or local storage).

---

### `migrations/` – Alembic Migrations

Manages schema migrations for the database:

- `alembic.ini`, `env.py`, `script.py.mako` – Alembic’s core config files.
- `versions/` – Auto-generated Python scripts that track and apply schema changes.

---

## 🧪 Technologies Used

- **Python + Flask** – Core web framework
- **PostgreSQL** – Relational database
- **SQLAlchemy + Alembic** – ORM and schema migration
- **Celery + Redis** – Background task processing
- **Twilio / Africa’s Talking** – Messaging integrations
- **Langchain** – AI interaction layer
- **Docker** – Containerization
- **Supervisor** – Production process manager

---

## 🛠 Setup Instructions (Basic)

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-org/connected-ltd-connected-api.git
   cd connected-ltd-connected-api
   ```

2. **Configure environment variables**:
   Create a `.env` file or set up your config file to load secrets (JWT keys, DB URL, etc.).

3. **Run with Docker**:

   ```bash
   docker build -t connected-api .
   docker run -p 5000:5000 connected-api
   ```

4. **Run migrations**:
   ```bash
   flask db upgrade
   ```

---

## 👨‍💻 Contribution Guide

- Write clean, modular code.
- Use type hints and docstrings.
- Follow the existing `controller-model-schema` structure.
- Write tests where possible.

---

## 📄 License

This project is currently **proprietary**, but is scheduled to be released under the **Apache 2.0 License** in Q3 2025.

---
