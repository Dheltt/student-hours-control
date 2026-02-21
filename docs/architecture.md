# Architecture Overview

## Architectural Pattern

The application follows the Repository Pattern combined with a Service Layer architecture.

## Layers Description

### Presentation Layer
Handles user interaction via a CLI interface.

### Service Layer
Contains business logic, validation rules, and use cases.

### Repository Layer
Responsible for database communication using SQLAlchemy.

### Database Layer
MySQL 8 running inside a Docker container.

## Design Principles

- Separation of concerns
- Maintainability
- Scalability
- Clean architecture principles