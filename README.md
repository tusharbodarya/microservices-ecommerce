# E-commerce Microservices System

This project demonstrates a microservices-based system for a simple e-commerce application. The system is divided into three microservices: user authentication, product management, and order processing.

## Architecture

- **User Authentication Service**: Manages user registration, login, and authentication.
- **Product Management Service**: Manages CRUD operations for products, with concurrency control.
- **Order Processing Service**: Manages order creation, viewing, and updates, with asynchronous communication.

## Setup

### Prerequisites

- Docker
- Docker Compose

### Running the System

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd ecommerce-microservices
    ```

2. Build and start the services using Docker Compose:
    ```bash
    docker-compose up --build
    ```

3. Access the services via the following URLs:
    - Auth Service: `http://localhost:5001`
    - Product Service: `http://localhost:5002`
    - Order Service: `http://localhost:5003`
    - RabbitMQ Management: `http://localhost:15672` (user: `guest`, password: `guest`)
    - Prometheus: `http://localhost:9090`
    - Grafana: `http://localhost:3000` (user: `admin`, password: `admin`)

## Testing

To run the tests, navigate to each service directory and execute:
```bash
pytest
